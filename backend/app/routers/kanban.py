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

from app.core.dependencies import (
    get_current_user
)

router = APIRouter(
    prefix="/tasks",
    tags=["Kanban"]
)




@router.get("/kanban")
def get_kanban(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    stmt = select(Task)

    result = db.execute(stmt)

    tasks = result.scalars().all()

    return {

        "todo": [
            task for task in tasks
            if task.status == "todo"
        ],

        "in_progress": [
            task for task in tasks
            if task.status == "in_progress"
        ],

        "review": [
            task for task in tasks
            if task.status == "review"
        ],

        "done": [
            task for task in tasks
            if task.status == "done"
        ]

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

    stmt = (
        select(Task)
        .where(Task.id == id)
    )

    result = db.execute(stmt)

    task = result.scalar_one_or_none()

    if not task:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task.status = payload.status

    db.commit()

    db.refresh(task)

    return task