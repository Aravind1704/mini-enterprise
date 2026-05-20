from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.task import (
    TaskOut
)

from app.core.dependencies import (
    get_current_user
)

from app.services.task_service import (
    list_tasks_service
)

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.get(
    "/",
    response_model=list[TaskOut]
)
def list_tasks(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):

    return list_tasks_service(
        db,
        user
    )