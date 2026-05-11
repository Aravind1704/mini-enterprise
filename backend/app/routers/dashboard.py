from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session
from sqlalchemy import (
    select,
    func
)

from app.database import get_db

from app.models.task import Task
from app.models.approval import Approval

from app.schemas.dashboard import (
    DashboardSummary,
    TaskDistribution
)

from app.core.dependencies import (
    get_current_user
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


# ----------------------------
# DASHBOARD SUMMARY
# ----------------------------

@router.get(
    "/summary",
    response_model=DashboardSummary
)
def get_summary(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    total_tasks = db.execute(
        select(func.count(Task.id))
    ).scalar()

    todo = db.execute(
        select(func.count(Task.id))
        .where(Task.status == "todo")
    ).scalar()

    in_progress = db.execute(
        select(func.count(Task.id))
        .where(Task.status == "in_progress")
    ).scalar()

    review = db.execute(
        select(func.count(Task.id))
        .where(Task.status == "review")
    ).scalar()

    done = db.execute(
        select(func.count(Task.id))
        .where(Task.status == "done")
    ).scalar()

    pending_approvals = db.execute(
        select(func.count(Approval.id))
        .where(Approval.status == "pending")
    ).scalar()

    return {
        "total_tasks": total_tasks,
        "todo": todo,
        "in_progress": in_progress,
        "review": review,
        "done": done,
        "pending_approvals": pending_approvals
    }




@router.get(
    "/task-distribution",
    response_model=list[TaskDistribution]
)
def task_distribution(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return [

        {
            "status": "todo",
            "count": db.execute(
                select(func.count(Task.id))
                .where(Task.status == "todo")
            ).scalar()
        },

        {
            "status": "in_progress",
            "count": db.execute(
                select(func.count(Task.id))
                .where(Task.status == "in_progress")
            ).scalar()
        },

        {
            "status": "review",
            "count": db.execute(
                select(func.count(Task.id))
                .where(Task.status == "review")
            ).scalar()
        },

        {
            "status": "done",
            "count": db.execute(
                select(func.count(Task.id))
                .where(Task.status == "done")
            ).scalar()
        }

    ]