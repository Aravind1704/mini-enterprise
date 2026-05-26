from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.analytics import (
    AnalyticsSummary,
    TaskStatusAnalytics,
    UserTaskAnalytics
)

from app.core.dependencies import (
    get_current_user
)

from app.services.analytics_service import (
    analytics_summary_service,
    task_status_analytics_service,
    user_task_analytics_service
)

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


# =====================================================
# ANALYTICS SUMMARY
# =====================================================

@router.get(
    "/summary",
    response_model=AnalyticsSummary
)
def analytics_summary(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):

    return analytics_summary_service(
        db,
        user
    )


# =====================================================
# TASK STATUS ANALYTICS
# =====================================================

@router.get(
    "/task-status",
    response_model=list[TaskStatusAnalytics]
)
def task_status_analytics(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):

    return task_status_analytics_service(
        db,
        user
    )


# =====================================================
# USER TASK ANALYTICS
# =====================================================

@router.get(
    "/user-tasks",
    response_model=list[UserTaskAnalytics]
)
def user_task_analytics(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):

    return user_task_analytics_service(
        db,
        user
    )