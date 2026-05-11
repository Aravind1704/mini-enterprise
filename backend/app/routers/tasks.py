from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import get_db

from app.models.task import Task

from app.schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskAssign,
    TaskOut
)

from app.schemas.kanban import (
    StatusUpdate
)

from app.core.dependencies import (
    get_current_user,
    require_role
)

from app.services.task_service import (
    create_task,
    get_all_tasks,
    get_task_by_id,
    update_task,
    delete_task,
    assign_task
)

from app.services.notification_service import (
    notify_task_assigned
)

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


# ----------------------------
# KANBAN BOARD
# ----------------------------

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


# ----------------------------
# UPDATE TASK STATUS
# ----------------------------

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


# ----------------------------
# CREATE TASK
# ----------------------------

@router.post(
    "/",
    response_model=TaskOut
)
def create(
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_role("admin", "manager")
    )
):

    return create_task(
        data,
        current_user.id,
        db
    )


# ----------------------------
# GET ALL TASKS
# ----------------------------

@router.get(
    "/",
    response_model=list[TaskOut]
)
def list_all(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return get_all_tasks(
        current_user.role,
        current_user.id,
        db
    )


# ----------------------------
# GET SINGLE TASK
# ----------------------------

@router.get(
    "/{id}",
    response_model=TaskOut
)
def get_one(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return get_task_by_id(
        id,
        db
    )


# ----------------------------
# UPDATE TASK
# ----------------------------

@router.put(
    "/{id}",
    response_model=TaskOut
)
def update(
    id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return update_task(
        id,
        data,
        current_user,
        db
    )


# ----------------------------
# DELETE TASK
# ----------------------------

@router.delete("/{id}")
def delete(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_role("admin", "manager")
    )
):

    return delete_task(
        id,
        db
    )


# ----------------------------
# ASSIGN TASK
# ----------------------------

@router.patch(
    "/{id}/assign",
    response_model=TaskOut
)
def assign(
    id: int,
    data: TaskAssign,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_role("admin", "manager")
    )
):

    task = assign_task(
    id,
    data.assigned_to_id,
    current_user,
    db
)

    # Send Notification

    if task.assigned_to_id:

        notify_task_assigned(
            task_id=task.id,
            assigned_to_id=task.assigned_to_id,
            assigned_by_name=current_user.name,
            db=db
        )

    return task
