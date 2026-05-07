from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.dependencies import require_role
from app.services.audit_service import get_audit_logs, get_recent_activity

router = APIRouter(prefix="/audit-logs", tags=["Audit"])

@router.get("/")
def list_audit_logs(db: Session = Depends(get_db), _=Depends(require_role("admin"))):
    return get_audit_logs(db)

@router.get("/activity")
def recent_activity(days: int = 7, db: Session = Depends(get_db), _=Depends(require_role("admin"))):
    return get_recent_activity(days, db)