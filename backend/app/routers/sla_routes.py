from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import Optional, List
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.sla import SLARuleCreate, SLARuleOut, SLARuleUpdate, SLATrackingOut
from app.services.sla_service import create_sla_rule, list_sla_rules, get_sla_rule, update_sla_rule, disable_sla_rule, start_sla_tracking, complete_sla, list_active_sla, list_breached_sla
from app.core.dependencies import get_current_user, require_admin

router = APIRouter(prefix="/sla-rules", tags=["SLA Rules"])

@router.post("/", response_model=SLARuleOut, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)])
def api_create_rule(payload: SLARuleCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return create_sla_rule(db, payload, created_by=current_user.id)

@router.get("/", response_model=List[SLARuleOut])
def api_list_rules(module_name: Optional[str] = Query(None), priority: Optional[str] = Query(None), active_only: Optional[bool] = Query(False), db: Session = Depends(get_db)):
    return list_sla_rules(db, module_name=module_name, priority=priority, active_only=active_only)

@router.get("/{rule_id}", response_model=SLARuleOut)
def api_get_rule(rule_id: int, db: Session = Depends(get_db)):
    rule = get_sla_rule(db, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="SLA rule not found")
    return rule

@router.put("/{rule_id}", response_model=SLARuleOut, dependencies=[Depends(require_admin)])
def api_update_rule(rule_id: int, payload: SLARuleUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    rule = get_sla_rule(db, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="SLA rule not found")
    return update_sla_rule(db, rule, payload)

@router.delete("/{rule_id}", response_model=SLARuleOut, dependencies=[Depends(require_admin)])
def api_disable_rule(rule_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    rule = get_sla_rule(db, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="SLA rule not found")
    return disable_sla_rule(db, rule)

# SLA tracking endpoints
tracking_router = APIRouter(prefix="/sla-tracking", tags=["SLA Tracking"])

@tracking_router.post("/tasks/{task_id}", response_model=SLATrackingOut)
def start_task_sla(task_id: int, db: Session = Depends(get_db)):
    st = start_sla_tracking(db, "task", task_id)
    if not st:
        raise HTTPException(status_code=404, detail="No SLA rule found for task")
    return st

@tracking_router.post("/approvals/{approval_id}", response_model=SLATrackingOut)
def start_approval_sla(approval_id: int, db: Session = Depends(get_db)):
    st = start_sla_tracking(db, "approval", approval_id)
    if not st:
        raise HTTPException(status_code=404, detail="No SLA rule found for approval")
    return st

@tracking_router.put("/{sla_id}/complete", response_model=SLATrackingOut)
def complete_sla_endpoint(sla_id: int, db: Session = Depends(get_db)):
    st = complete_sla(db, sla_id)
    if not st:
        raise HTTPException(status_code=404, detail="SLA record not found")
    return st

@tracking_router.get("/active", response_model=List[SLATrackingOut])
def get_active(db: Session = Depends(get_db)):
    return list_active_sla(db)

@tracking_router.get("/breached", response_model=List[SLATrackingOut])
def get_breached(db: Session = Depends(get_db)):
    return list_breached_sla(db)

@tracking_router.get("/record/{module_name}/{record_id}", response_model=List[SLATrackingOut])
def get_record_sla(module_name: str, record_id: int, db: Session = Depends(get_db)):
    return db.query(SLATracking).filter(SLATracking.module_name==module_name, SLATracking.record_id==record_id).all()
