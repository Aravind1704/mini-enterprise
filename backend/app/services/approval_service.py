from app.repositories import (
    approval_repo as repo
)


# =====================================================
# LIST APPROVALS SERVICE
# =====================================================

def list_approvals_service(
    db,
    user
):

    if user.role == "employee":

        return repo.list_employee_approvals(
            db,
            user.id
        )

    elif user.role == "manager":

        return repo.list_manager_approvals(
            db
        )

    return repo.list_all_approvals(
        db
    )