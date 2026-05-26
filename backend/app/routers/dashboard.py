from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.dashboard import DashboardSummary, TaskDistribution
from app.core.dependencies import get_current_user
from app.services.dashboard_service import (
    dashboard_summary_service,
    task_distribution_service,
    role_dashboard_service
)

# Prefix is EMPTY so /role-dashboard is available at the root level
router = APIRouter(
    prefix="",
    tags=["Dashboard"]
)

@router.get("/dashboard/summary", response_model=DashboardSummary)
def dashboard_summary(db: Session = Depends(get_db), user = Depends(get_current_user)):
    return dashboard_summary_service(db, user)

@router.get("/role-dashboard")
def role_dashboard(db: Session = Depends(get_db), user = Depends(get_current_user)):
    return role_dashboard_service(db, user)