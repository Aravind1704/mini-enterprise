from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.approval import Approval, ApprovalHistory
from app.schemas.approval import ApprovalCreate, ApprovalAction

def create_approval(data: ApprovalCreate, user_id: int, db: Session):
    approval = Approval(
        title=data.title,
        description=data.description,
        requested_by=user_id,
        status="pending",
        current_level="manager"
    )
    db.add(approval)
    db.commit()
    db.refresh(approval)
    return approval

def get_approvals(role: str, user_id: int, db: Session):
    if role == "admin":
        return db.query(Approval).all()
    elif role == "manager":
        return db.query(Approval).filter(Approval.current_level == "manager").all()
    else:
        return db.query(Approval).filter(Approval.requested_by == user_id).all()

def process_approval(approval_id: int, data: ApprovalAction, user, db: Session):
    approval = db.query(Approval).filter(Approval.id == approval_id).first()
    if not approval:
        raise HTTPException(status_code=404, detail="Approval not found")

    # Validate rejection has comment
    if data.action == "rejected" and not data.comment:
        raise HTTPException(status_code=400, detail="Comment is required for rejection")

    # Role-based action control
    if user.role == "manager" and approval.current_level != "manager":
        raise HTTPException(status_code=403, detail="Not your level to approve")

    # Update approval
    if data.action == "approved" and approval.current_level == "manager":
        approval.current_level = "admin"   # escalate to admin
        approval.status = "pending"
    elif data.action == "approved" and approval.current_level == "admin":
        approval.status = "approved"
    else:
        approval.status = data.action  # rejected or hold

    # Log history
    history = ApprovalHistory(
        approval_id=approval_id,
        action_by=user.id,
        action=data.action,
        comment=data.comment
    )
    db.add(history)
    db.commit()
    db.refresh(approval)
    return approval

def get_approval_history(approval_id: int, db: Session):
    return db.query(ApprovalHistory).filter(
        ApprovalHistory.approval_id == approval_id
    ).all()