from app.repositories import (
    task_repo as repo
)


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