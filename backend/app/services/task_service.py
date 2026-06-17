from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories import (
    task_repo as repo
)

from app.models.audit import AuditLog
from app.repositories.audit_repo import AuditRepo


def _ensure_task_tenant(task, user):
    if not task:
        return
    if user.role == "super_admin":
        return
    if task.tenant_id is not None and task.tenant_id != user.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cross-tenant access is not allowed"
        )


# =====================================================
# CREATE TASK SERVICE
# =====================================================

def create_task_service(
    db: Session,
    payload,
    user
):

    task_data = {

        "tenant_id": user.tenant_id,

        "title": payload.title,

        "description": payload.description,

        "priority": payload.priority,

        "due_date": payload.due_date,

        "assigned_to_id": payload.assigned_to_id,

        "created_by_id": user.id
    }

    task = repo.create_task(
        db,
        task_data
    )

    # =================================================
    # CREATE AUDIT LOG
    # =================================================

    AuditRepo.create(
        db,
        AuditLog(
            user_id=user.id,
            action="create",
            entity="task",
            entity_id=task.id,
            details=f"Task '{task.title}' created"
        )
    )

    return task

# =====================================================
# GET TASK BY ID
# =====================================================

def get_task_service(
    db: Session,
    task_id: int,
    user
):

    task = repo.get_task_by_id(
        task_id,
        db
    )
    _ensure_task_tenant(task, user)
    return task

# =====================================================
# UPDATE TASK
# =====================================================

def update_task_service(
    db: Session,
    task_id: int,
    payload,
    user
):

    task = repo.get_task_by_id(
        task_id,
        db
    )
    _ensure_task_tenant(task, user)

    task_data = payload.dict(exclude_unset=True)

    task = repo.update_task(
        db,
        task_id,
        task_data
    )

    if task:

        AuditRepo.create(
            db,
            AuditLog(
                user_id=user.id,
                action="update",
                entity="task",
                entity_id=task.id,
                details=f"Task '{task.title}' updated"
            )
        )

    return task


# =====================================================
# DELETE TASK
# =====================================================

def delete_task_service(
    db: Session,
    task_id: int,
    user
):

    task = repo.get_task_by_id(task_id, db)
    _ensure_task_tenant(task, user)

    task = repo.delete_task(db, task_id)

    if task:

        AuditRepo.create(
            db,
            AuditLog(
                user_id=user.id,
                action="delete",
                entity="task",
                entity_id=task.id,
                details=f"Task '{task.title}' deleted"
            )
        )

    return task

# =====================================================
# LIST TASKS
# =====================================================

def list_tasks_service(
    db,
    user
):

    if user.role == "employee":

        return repo.list_tasks_for_employee(
            db,
            user.id,
            user.tenant_id
        )

    elif user.role == "manager":

        return repo.list_tasks_for_manager(
            db,
            user.id,
            user.tenant_id
        )

    if user.role != "super_admin" and user.tenant_id is not None:
        return repo.list_tasks_by_tenant(
            db,
            user.tenant_id
        )

    return repo.list_all_tasks(db)
