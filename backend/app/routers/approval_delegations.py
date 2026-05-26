from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.database import get_db
from app.schemas.approval_delegation import ApprovalDelegationCreate, ApprovalDelegationOut
from app.services.approval_delegation_service import create_delegation, my_delegations, active_delegations, cancel_delegation
from app.core.dependencies import get_current_user, require_manager

router = APIRouter(prefix="/approval-delegations", tags=["Approval Delegations"])

@router.post("/", response_model=ApprovalDelegationOut, dependencies=[Depends(require_manager)])
def api_create_delegation(payload: ApprovalDelegationCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        d = create_delegation(db, current_user.id, payload.delegatee_id, payload.start_date, payload.end_date, payload.reason)
        return d
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/me", response_model=List[ApprovalDelegationOut])
def api_my_delegations(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return my_delegations(db, current_user.id)

@router.get("/active", response_model=List[ApprovalDelegationOut])
def api_active_delegations(db: Session = Depends(get_db)):
    return active_delegations(db)

@router.put("/{id}/cancel", response_model=ApprovalDelegationOut, dependencies=[Depends(require_manager)])
def api_cancel_delegation(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    d = cancel_delegation(db, id, current_user.id)
    if not d:
        raise HTTPException(status_code=404, detail="Delegation not found")
    return d
