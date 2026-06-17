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
            user.id,
            user.tenant_id
        )

    elif user.role == "manager":

        return repo.list_manager_approvals(
            db,
            user.tenant_id
        )

    if user.role != "super_admin" and user.tenant_id is not None:
        return repo.list_all_approvals(
            db,
            user.tenant_id
        )

    return repo.list_all_approvals(
        db
    )
