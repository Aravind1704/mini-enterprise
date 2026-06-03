from datetime import datetime

from sqlalchemy.orm import Session

from app.database import SessionLocal

from app.models.sla import (
    SLATracking,
    SLARule
)

from app.models.approval import Approval

from app.models.approval_escalation import (
    ApprovalEscalation
)

from app.services.approval_escalation_service import (
    create_escalation
)


# =========================================
# SLA MONITOR
# =========================================

def monitor_sla():

    print("SLA MONITOR RUNNING")

    db: Session = SessionLocal()

    try:

        # =====================================
        # GET ACTIVE SLA RECORDS
        # =====================================

        active_slas = (
            db.query(SLATracking)
            .filter(
                SLATracking.status == "active"
            )
            .all()
        )

        now = datetime.utcnow()

        for sla in active_slas:

            print(f"CHECKING SLA ID: {sla.id}")

            # =====================================
            # SLA RULE
            # =====================================

            rule = (
                db.query(SLARule)
                .filter(
                    SLARule.id ==
                    sla.sla_rule_id
                )
                .first()
            )

            if not rule:

                print("NO SLA RULE FOUND")

                continue

            # =====================================
            # BREACH CHECK
            # =====================================

            if now >= sla.due_time:

                print("SLA BREACHED")

                sla.status = "breached"

                if not sla.breach_reason:

                    sla.breach_reason = (
                        "SLA deadline exceeded"
                    )

                db.add(sla)

            # =====================================
            # ESCALATION DISABLED
            # =====================================

            if not rule.escalation_enabled:

                print("ESCALATION DISABLED")

                continue

            # =====================================
            # TIME PASSED
            # =====================================

            hours_passed = (
                now - sla.start_time
            ).total_seconds() / 3600

            print(
                f"HOURS PASSED: {hours_passed}"
            )

            # =====================================
            # ESCALATION TIME CHECK
            # =====================================

            if (
                hours_passed <
                rule.escalation_after_hours
            ):

                print("ESCALATION TIME NOT REACHED")

                continue

            # =====================================
            # APPROVAL MODULE
            # =====================================

            if sla.module_name == "approval":

                approval = (
                    db.query(Approval)
                    .filter(
                        Approval.id ==
                        sla.record_id
                    )
                    .first()
                )

                if not approval:

                    print("APPROVAL NOT FOUND")

                    continue

                # =================================
                # ALREADY ESCALATED?
                # =================================

                existing = (
                    db.query(
                        ApprovalEscalation
                    )
                    .filter(
                        ApprovalEscalation.approval_id
                        == approval.id,

                        ApprovalEscalation.status
                        == "pending"
                    )
                    .first()
                )

                if existing:

                    print(
                        "ESCALATION ALREADY EXISTS"
                    )

                    continue

                print(
                    "CREATING APPROVAL ESCALATION"
                )

                # =================================
                # CREATE ESCALATION
                # =================================

                create_escalation(
                    db=db,
                    approval_id=approval.id,
                    escalated_from=1,
                    escalated_to=1,
                    reason="SLA breached automatically",
                    escalation_level=1
                )

            # =====================================
            # TASK MODULE
            # =====================================

            elif sla.module_name == "task":

                print(
                    f"TASK {sla.record_id} BREACHED"
                )

        db.commit()

        print("SLA MONITOR COMPLETED")

    except Exception as e:

        print("SLA MONITOR ERROR:", e)

        import traceback

        traceback.print_exc()

        db.rollback()

    finally:

        db.close()