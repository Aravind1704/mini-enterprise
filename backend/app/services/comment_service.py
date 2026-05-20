from fastapi import HTTPException

from app.repositories import (
    comment_repo as repo
)

from app.services.notification_service import (
    notify_comment_added
)


# =====================================================
# CREATE COMMENT
# =====================================================

def create_comment_service(
    task_id,
    data,
    db,
    user
):

    task = repo.get_task_by_id(
        task_id,
        db
    )

    if not task:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if (
        data.is_internal
        and user.role == "employee"
    ):

        raise HTTPException(
            status_code=403,
            detail="Employees cannot add internal notes"
        )

    comment = repo.create_comment(
        task_id=task_id,
        user_id=user.id,
        content=data.content,
        is_internal=data.is_internal,
        db=db
    )

    if (
        task.assigned_to_id
        and task.assigned_to_id != user.id
    ):

        notify_comment_added(
            task_id=task.id,
            task_title=task.title,
            commenter_name=user.name,
            assigned_to_id=task.assigned_to_id,
            db=db
        )

    return comment


# =====================================================
# LIST COMMENTS
# =====================================================

def list_comments_service(
    task_id,
    db,
    user
):

    if user.role == "employee":

        return repo.list_comments_for_employee(
            task_id,
            db
        )

    elif user.role == "manager":

        return repo.list_comments_for_manager(
            task_id,
            db
        )

    return repo.list_all_comments(
        task_id,
        db
    )