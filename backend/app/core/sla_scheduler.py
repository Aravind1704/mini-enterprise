from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from app.database import SessionLocal
from app.models.sla import SLATracking
from app.models.approval import Approval
from app.models.task import Task
from app.models.approval import Approval as ApprovalModel
from app.models.approval_escalation import ApprovalEscalation  # create model file if not present
from app.services.notification_service import notify_user  # reuse your notification service

def check_sla_breaches():
    db = SessionLocal()
    try:
        now = datetime.utcnow()
        rows = db.query(SLATracking).filter(SLATracking.status == "active", SLATracking.due_time < now).all()
        for r in rows:
            r.status = "breached"
            r.breach_reason = "Due time passed"
            db.add(r)
            # update related record flags
            if r.module_name == "task":
                task = db.query(Task).get(r.record_id)
                if task:
                    task.is_sla_breached = True
                    db.add(task)
                    # notify assignee
                    if task.assigned_to_id:
                        notify_user(task.assigned_to_id, f"Task {task.id} breached SLA")
            elif r.module_name == "approval":
                approval = db.query(ApprovalModel).get(r.record_id)
                if approval:
                    approval.is_escalated = True
                    db.add(approval)
                    # create escalation record (simple auto-escalation)
                    esc = ApprovalEscalation(approval_id=approval.id, escalated_from=approval.requested_by, escalated_to=None, reason="Auto escalation due to SLA breach", escalation_level=1, status="pending")
                    db.add(esc)
                    # notify admins/managers (example: notify requester)
                    notify_user(approval.requested_by, f"Approval {approval.id} breached SLA and was escalated")
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_sla_breaches, "interval", seconds=60, id="sla_breach_check")
    scheduler.start()
