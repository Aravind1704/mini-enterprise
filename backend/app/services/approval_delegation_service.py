from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.models.approval_delegation import ApprovalDelegation
from app.repositories.approval_delegation_repo import ApprovalDelegationRepo
from app.repositories.audit_repo import AuditRepo
from app.models.audit import AuditLog

def create_delegation(db: Session, delegator_id: int, delegatee_id: int, start_date: datetime, end_date: datetime, reason: str) -> ApprovalDelegation:
    # validate dates
    if end_date <= start_date:
        raise ValueError("end_date must be after start_date")
    # check conflicts (simple)
    existing = db.query(ApprovalDelegation).filter(
        ApprovalDelegation.delegator_id == delegator_id,
        ApprovalDelegation.is_active == True,
        ApprovalDelegation.end_date >= start_date,
        ApprovalDelegation.start_date <= end_date
    ).first()
    if existing:
        raise ValueError("Delegation conflict with existing active delegation")

    d = ApprovalDelegation(
        delegator_id=delegator_id,
        delegatee_id=delegatee_id,
        start_date=start_date,
        end_date=end_date,
        reason=reason,
        is_active=True
    )
    d = ApprovalDelegationRepo.create(db, d)

    AuditRepo.create(db, AuditLog(
        user_id=delegator_id,
        module_name="delegation",
        action_type="delegation_created",
        record_id=d.id,
        details=f"Delegated to {delegatee_id} from {start_date} to {end_date}"
    ))
    return d

def my_delegations(db: Session, delegator_id: int) -> List[ApprovalDelegation]:
    return ApprovalDelegationRepo.list_for_delegator(db, delegator_id)

def active_delegations(db: Session) -> List[ApprovalDelegation]:
    return ApprovalDelegationRepo.list_active(db)

def cancel_delegation(db: Session, id: int, user_id: int) -> Optional[ApprovalDelegation]:
    d = ApprovalDelegationRepo.get(db, id)
    if not d:
        return None
    d.is_active = False
    d = ApprovalDelegationRepo.save(db, d)
    AuditRepo.create(db, AuditLog(
        user_id=user_id,
        module_name="delegation",
        action_type="delegation_cancelled",
        record_id=d.id,
        details=f"Delegation cancelled by {user_id}"
    ))
    return d
