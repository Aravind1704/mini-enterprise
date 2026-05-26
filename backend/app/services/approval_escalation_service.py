from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from app.models.approval_escalation import ApprovalEscalation
from app.repositories.approval_escalation_repo import ApprovalEscalationRepo
from app.models.approval import Approval
from app.repositories.audit_repo import AuditRepo
from app.models.audit import AuditLog

def create_escalation(db: Session, approval_id: int, escalated_from: int, escalated_to: Optional[int], reason: str, escalation_level: int = 1) -> ApprovalEscalation:
    esc = ApprovalEscalation(
        approval_id=approval_id,
        escalated_from=escalated_from,
        escalated_to=escalated_to,
        reason=reason,
        escalation_level=escalation_level,
        status="pending",
        escalated_at=datetime.utcnow()
    )
    esc = ApprovalEscalationRepo.create(db, esc)

    # update approval flags
    approval = db.query(Approval).get(approval_id)
    if approval:
        approval.is_escalated = True
        approval.current_escalation_to = escalated_to
        db.add(approval)
        db.commit()

    # audit
    try:
        AuditRepo.create(db, AuditLog(
            user_id=escalated_from,
            module_name="approval",
            action_type="escalation_created",
            record_id=approval_id,
            details=f"Escalated to {escalated_to} level {escalation_level}"
        ))
    except Exception:
        db.rollback()

    return esc

def list_escalations(db: Session) -> List[ApprovalEscalation]:
    return ApprovalEscalationRepo.list_all(db)

def list_pending(db: Session) -> List[ApprovalEscalation]:
    return ApprovalEscalationRepo.list_pending(db)

def list_for_approval(db: Session, approval_id: int) -> List[ApprovalEscalation]:
    return ApprovalEscalationRepo.list_for_approval(db, approval_id)

def resolve_escalation(db: Session, esc_id: int, resolver_id: int) -> Optional[ApprovalEscalation]:
    esc = ApprovalEscalationRepo.get(db, esc_id)
    if not esc:
        return None
    esc.status = "resolved"
    esc.resolved_at = datetime.utcnow()
    esc = ApprovalEscalationRepo.save(db, esc)

    # update approval
    approval = db.query(Approval).get(esc.approval_id)
    if approval:
        approval.is_escalated = False
        approval.current_escalation_to = None
        db.add(approval)
        db.commit()

    # audit
    AuditRepo.create(db, AuditLog(
        user_id=resolver_id,
        module_name="approval",
        action_type="escalation_resolved",
        record_id=esc.approval_id,
        details=f"Escalation {esc_id} resolved by {resolver_id}"
    ))
    return esc

def cancel_escalation(db: Session, esc_id: int, canceller_id: int) -> Optional[ApprovalEscalation]:
    esc = ApprovalEscalationRepo.get(db, esc_id)
    if not esc:
        return None
    esc.status = "cancelled"
    esc.resolved_at = datetime.utcnow()
    esc = ApprovalEscalationRepo.save(db, esc)

    approval = db.query(Approval).get(esc.approval_id)
    if approval:
        approval.is_escalated = False
        approval.current_escalation_to = None
        db.add(approval)
        db.commit()

    AuditRepo.create(db, AuditLog(
        user_id=canceller_id,
        module_name="approval",
        action_type="escalation_cancelled",
        record_id=esc.approval_id,
        details=f"Escalation {esc_id} cancelled by {canceller_id}"
    ))
    return esc
