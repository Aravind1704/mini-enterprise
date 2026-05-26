from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.task import (
<<<<<<< HEAD
    TaskCreate,
    TaskUpdate,
=======
>>>>>>> 4500000c8c54ec045a9125ffb74854e6cb5209d2
    TaskOut
)

from app.core.dependencies import (
    get_current_user
)

from app.services.task_service import (
<<<<<<< HEAD
    create_task_service,
    list_tasks_service,
    get_task_service,
    update_task_service,
    delete_task_service
=======
    list_tasks_service
>>>>>>> 4500000c8c54ec045a9125ffb74854e6cb5209d2
)

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


<<<<<<< HEAD
# =====================================================
# CREATE TASK
# =====================================================

@router.post(
    "/",
    response_model=TaskOut
)
def create_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    return create_task_service(
        db,
        payload,
        user
    )


# =====================================================
# LIST TASKS
# =====================================================

=======
>>>>>>> 4500000c8c54ec045a9125ffb74854e6cb5209d2
@router.get(
    "/",
    response_model=list[TaskOut]
)
def list_tasks(
    db: Session = Depends(get_db),
<<<<<<< HEAD
    user=Depends(get_current_user)
=======
    user = Depends(get_current_user)
>>>>>>> 4500000c8c54ec045a9125ffb74854e6cb5209d2
):

    return list_tasks_service(
        db,
        user
<<<<<<< HEAD
    )


# =====================================================
# GET TASK BY ID
# =====================================================

@router.get(
    "/{task_id}",
    response_model=TaskOut
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    task = get_task_service(
        db,
        task_id
    )

    if not task:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


# =====================================================
# UPDATE TASK
# =====================================================

@router.put(
    "/{task_id}",
    response_model=TaskOut
)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    task = update_task_service(
        db,
        task_id,
        payload,
        user
    )

    if not task:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


# =====================================================
# DELETE TASK
# =====================================================

@router.delete(
    "/{task_id}"
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    task = delete_task_service(
        db,
        task_id,
        user
    )

    if not task:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "message": "Task deleted successfully"
    }
=======
    )
>>>>>>> 4500000c8c54ec045a9125ffb74854e6cb5209d2
