from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.approval_escalation import ApprovalEscalationCreate, ApprovalEscalationOut
from app.services.approval_escalation_service import create_escalation, list_escalations, list_pending, list_for_approval, resolve_escalation, cancel_escalation
from app.core.dependencies import get_current_user, require_manager
from app.models.user import User
from app.schemas.user import UserOut

router = APIRouter(prefix="/approval-escalations", tags=["Approval Escalations"])

@router.post("/", response_model=ApprovalEscalationOut, dependencies=[Depends(require_manager)])
def api_create_escalation(payload: ApprovalEscalationCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        esc = create_escalation(db, payload.approval_id, current_user.id, payload.escalated_to, payload.reason, payload.escalation_level)
        return esc
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
@router.get(
    "/users",
    response_model=List[UserOut]
)
def get_users(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return (
        db.query(User)
        .filter(
            User.role.in_([
                "admin",
                "manager"
            ])
        )
        .all()
    )

@router.get("/", response_model=List[ApprovalEscalationOut])
def api_list_escalations(db: Session = Depends(get_db)):
    return list_escalations(db)

@router.get("/pending", response_model=List[ApprovalEscalationOut])
def api_list_pending(db: Session = Depends(get_db)):
    return list_pending(db)

@router.get("/approval/{approval_id}", response_model=List[ApprovalEscalationOut])
def api_history_for_approval(approval_id: int, db: Session = Depends(get_db)):
    return list_for_approval(db, approval_id)

@router.put("/{id}/resolve", response_model=ApprovalEscalationOut, dependencies=[Depends(require_manager)])
def api_resolve(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    esc = resolve_escalation(db, id, current_user.id)
    if not esc:
        raise HTTPException(status_code=404, detail="Escalation not found")
    return esc

@router.put("/{id}/cancel", response_model=ApprovalEscalationOut, dependencies=[Depends(require_manager)])
def api_cancel(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    esc = cancel_escalation(db, id, current_user.id)
    if not esc:
        raise HTTPException(status_code=404, detail="Escalation not found")
    return esc
