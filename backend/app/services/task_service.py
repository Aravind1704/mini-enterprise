from sqlalchemy.orm import Session

from app.repositories import (
    task_repo as repo
)

from app.models.audit import AuditLog
from app.repositories.audit_repo import AuditRepo


# =====================================================
# CREATE TASK SERVICE
# =====================================================

def create_task_service(
    db: Session,
    payload,
    user
):

    task_data = {

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
    task_id: int
):

    return repo.get_task_by_id(
        task_id,
        db
    )

# =====================================================
# UPDATE TASK
# =====================================================

def update_task_service(
    db: Session,
    task_id: int,
    payload,
    user
):

    task_data = payload.dict(
        exclude_unset=True
    )

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

    task = repo.delete_task(
        db,
        task_id
    )

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
            user.id
        )

    elif user.role == "manager":

        return repo.list_tasks_for_manager(
            db,
            user.id
        )


    return repo.list_all_tasks(db)