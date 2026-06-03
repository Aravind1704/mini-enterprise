from datetime import datetime, timedelta
from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.sla import SLARule, SLATracking
from app.schemas.sla import SLARuleCreate, SLARuleUpdate

def create_sla_rule(db: Session, payload: SLARuleCreate, created_by: Optional[int] = None) -> SLARule:
    rule = SLARule(
        module_name=payload.module_name,
        priority=payload.priority,
        allowed_hours=payload.allowed_hours,
        escalation_enabled=payload.escalation_enabled,
        escalation_after_hours=payload.escalation_after_hours,
        is_active=payload.is_active,
        created_by=created_by
    )
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule

def list_sla_rules(db: Session, module_name: Optional[str]=None, priority: Optional[str]=None, active_only: bool=False) -> List[SLARule]:
    q = db.query(SLARule)
    if module_name:
        q = q.filter(SLARule.module_name == module_name)
    if priority:
        q = q.filter(SLARule.priority == priority)
    if active_only:
        q = q.filter(SLARule.is_active == True)
    return q.order_by(SLARule.id.desc()).all()

def get_sla_rule(db: Session, rule_id: int) -> Optional[SLARule]:
    return db.query(SLARule).filter(SLARule.id == rule_id).first()

def update_sla_rule(db: Session, rule: SLARule, payload: SLARuleUpdate) -> SLARule:
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(rule, k, v)
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule

def disable_sla_rule(db: Session, rule: SLARule) -> SLARule:
    rule.is_active = False
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule

def start_sla_tracking(
    db: Session,
    module_name: str,
    record_id: int
) -> Optional[SLATracking]:

    rule = (
        db.query(SLARule)
        .filter(
            SLARule.module_name == module_name,
            SLARule.is_active == True
        )
        .order_by(
            SLARule.allowed_hours
        )
        .first()
    )

    if not rule:
        return None

    start = datetime.utcnow()

    # =====================================
    # REAL SLA TIME
    # =====================================

    due = start + timedelta(
        hours=rule.allowed_hours
    )

    st = SLATracking(
        module_name=module_name,
        record_id=record_id,
        sla_rule_id=rule.id,
        start_time=start,
        due_time=due,
        status="active"
    )

    db.add(st)

    db.commit()

    db.refresh(st)

    return st

def complete_sla(db: Session, sla_id: int) -> Optional[SLATracking]:
    st = db.query(SLATracking).get(sla_id)
    if not st:
        return None
    st.completed_time = datetime.utcnow()
    st.status = "completed"
    db.add(st)
    db.commit()
    db.refresh(st)
    return st


# =========================================
# ACTIVE SLA
# =========================================

def list_active_sla(db: Session):

    now = datetime.utcnow()

    # =====================================
    # AUTO MOVE BREACHED RECORDS
    # =====================================

    expired_records = (
        db.query(SLATracking)
        .filter(
            SLATracking.status == "active",
            SLATracking.due_time <= now
        )
        .all()
    )

    for item in expired_records:

        item.status = "breached"

        if not item.breach_reason:

            item.breach_reason = (
                "SLA deadline exceeded"
            )

        db.add(item)

    db.commit()

    # =====================================
    # RETURN ONLY ACTIVE
    # =====================================

    active_records = (
        db.query(SLATracking)
        .filter(
            SLATracking.status == "active",
            SLATracking.due_time > now
        )
        .order_by(
            SLATracking.id.desc()
        )
        .all()
    )

    return active_records

# =========================================
# BREACHED SLA
# =========================================

def list_breached_sla(db: Session):

    now = datetime.utcnow()

    breached_records = (
        db.query(SLATracking)
        .filter(
            SLATracking.due_time <= now
        )
        .all()
    )

    for item in breached_records:

        if item.status != "breached":

            item.status = "breached"

            item.breach_reason = (
                "SLA deadline exceeded"
            )

            db.add(item)

    db.commit()

    return (
        db.query(SLATracking)
        .filter(
            SLATracking.status == "breached"
        )
        .order_by(
            SLATracking.id.desc()
        )
        .all()
    )