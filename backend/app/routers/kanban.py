from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import get_db
from app.models.task import Task
from app.schemas.kanban import (
    TaskOut,
    StatusUpdate
)
from app.schemas.task import TaskOut
from app.core.dependencies import (
    get_current_user
)

router = APIRouter(
    prefix="/tasks",
    tags=["Kanban"]
)


@router.get(
    "/kanban",
    response_model=dict[str, list[TaskOut]]
)
def get_kanban(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    tasks = db.execute(
        select(Task)
    ).scalars().all()

    return {
        "todo": [t for t in tasks if t.status == "todo"],
        "in_progress": [t for t in tasks if t.status == "in_progress"],
        "review": [t for t in tasks if t.status == "review"],
        "done": [t for t in tasks if t.status == "done"]
    }


@router.patch(
    "/{id}/status",
    response_model=TaskOut
)
def update_status(
    id: int,
    payload: StatusUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    task = db.execute(
        select(Task).where(Task.id == id)
    ).scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task.status = payload.status

    db.commit()
    db.refresh(task)

    return task