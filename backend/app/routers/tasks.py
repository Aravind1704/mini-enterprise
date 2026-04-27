from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.task import TaskCreate, TaskUpdate, TaskAssign, TaskOut
from app.core.dependencies import get_current_user, require_role
from app.services.task_service import (
    create_task, get_all_tasks, get_task_by_id,
    update_task, delete_task, assign_task
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskOut)
def create(data: TaskCreate, db: Session = Depends(get_db), current_user=Depends(require_role("admin", "manager"))):
    return create_task(data, current_user.id, db)


@router.get("/", response_model=list[TaskOut])
def list_all(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_all_tasks(current_user.role, current_user.id, db)


@router.get("/{id}", response_model=TaskOut)
def get_one(id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return get_task_by_id(id, db)


@router.put("/{id}", response_model=TaskOut)
def update(id: int, data: TaskUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return update_task(id, data, current_user, db)


@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db), _=Depends(require_role("admin", "manager"))):
    return delete_task(id, db)


@router.patch("/{id}/assign", response_model=TaskOut)
def assign(id: int, data: TaskAssign, db: Session = Depends(get_db), _=Depends(require_role("admin", "manager"))):
    return assign_task(id, data.assigned_to_id, db)