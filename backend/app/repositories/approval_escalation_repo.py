from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.approval_escalation import ApprovalEscalation

class ApprovalEscalationRepo:
    @staticmethod
    def create(db: Session, esc: ApprovalEscalation) -> ApprovalEscalation:
        db.add(esc)
        db.commit()
        db.refresh(esc)
        return esc

    @staticmethod
    def get(db: Session, id: int) -> Optional[ApprovalEscalation]:
        return db.query(ApprovalEscalation).get(id)

    @staticmethod
    def list_all(db: Session) -> List[ApprovalEscalation]:
        return db.query(ApprovalEscalation).order_by(ApprovalEscalation.escalated_at.desc()).all()

    @staticmethod
    def list_pending(db: Session) -> List[ApprovalEscalation]:
        return db.query(ApprovalEscalation).filter(ApprovalEscalation.status == "pending").all()

    @staticmethod
    def list_for_approval(db: Session, approval_id: int) -> List[ApprovalEscalation]:
        return db.query(ApprovalEscalation).filter(ApprovalEscalation.approval_id == approval_id).order_by(ApprovalEscalation.escalated_at.desc()).all()

    @staticmethod
    def save(db: Session, esc: ApprovalEscalation) -> ApprovalEscalation:
        db.add(esc)
        db.commit()
        db.refresh(esc)
        return esc
