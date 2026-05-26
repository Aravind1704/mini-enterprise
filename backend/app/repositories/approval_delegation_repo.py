from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.approval_delegation import ApprovalDelegation
from datetime import datetime

class ApprovalDelegationRepo:
    @staticmethod
    def create(db: Session, delegation: ApprovalDelegation) -> ApprovalDelegation:
        db.add(delegation)
        db.commit()
        db.refresh(delegation)
        return delegation

    @staticmethod
    def get(db: Session, id: int) -> Optional[ApprovalDelegation]:
        return db.query(ApprovalDelegation).get(id)

    @staticmethod
    def list_for_delegator(db: Session, delegator_id: int) -> List[ApprovalDelegation]:
        return db.query(ApprovalDelegation).filter(ApprovalDelegation.delegator_id == delegator_id).order_by(ApprovalDelegation.created_at.desc()).all()

    @staticmethod
    def list_active(db: Session, now: datetime = None) -> List[ApprovalDelegation]:
        if now is None:
            now = datetime.utcnow()
        return db.query(ApprovalDelegation).filter(ApprovalDelegation.is_active == True, ApprovalDelegation.start_date <= now, ApprovalDelegation.end_date >= now).all()

    @staticmethod
    def save(db: Session, delegation: ApprovalDelegation) -> ApprovalDelegation:
        db.add(delegation)
        db.commit()
        db.refresh(delegation)
        return delegation
