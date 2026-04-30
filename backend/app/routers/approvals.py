from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.approval import Approval, ApprovalHistory
from app.core.dependencies import get_current_user, require_role
from pydantic import BaseModel
from typing import Optional

class ApprovalCreate(BaseModel):
    title: str
    description: Optional[str] = None

class ApprovalAction(BaseModel):
    action: str
    comment: Optional[str] = None

router = APIRouter(prefix="/approvals", tags=["Approvals"])

@router.post("/")
def submit_approval(data: ApprovalCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    approval = Approval(title=data.title, description=data.description, requested_by=current_user.id)
    db.add(approval)
    db.commit()
    db.refresh(approval)
    return {"id": approval.id, "title": approval.title, "description": approval.description, "requested_by": approval.requested_by, "status": approval.status, "current_level": approval.current_level, "created_at": approval.created_at}

@router.get("/")
def list_approvals(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role == "admin":
        approvals = db.query(Approval).all()
    elif current_user.role == "manager":
        approvals = db.query(Approval).filter(Approval.current_level == "manager").all()
    else:
        approvals = db.query(Approval).filter(Approval.requested_by == current_user.id).all()
    return [{"id": a.id, "title": a.title, "description": a.description, "requested_by": a.requested_by, "status": a.status, "current_level": a.current_level, "created_at": a.created_at} for a in approvals]

@router.patch("/{id}/action")
def action_approval(id: int, data: ApprovalAction, db: Session = Depends(get_db), current_user=Depends(require_role("admin", "manager"))):
    approval = db.query(Approval).filter(Approval.id == id).first()
    if not approval:
        raise HTTPException(status_code=404, detail="Approval not found")
    if data.action == "rejected" and not data.comment:
        raise HTTPException(status_code=400, detail="Comment required for rejection")
    approval.status = data.action
    history = ApprovalHistory(approval_id=id, action_by=current_user.id, action=data.action, comment=data.comment)
    db.add(history)
    db.commit()
    db.refresh(approval)
    return {"id": approval.id, "title": approval.title, "status": approval.status}

@router.get("/{id}/history")
def approval_history(id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    history = db.query(ApprovalHistory).filter(ApprovalHistory.approval_id == id).all()
    return [{"id": h.id, "approval_id": h.approval_id, "action_by": h.action_by, "action": h.action, "comment": h.comment, "created_at": h.created_at} for h in history]