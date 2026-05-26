from app.repositories import (
    dashboard_repo as repo
)


# =====================================================
# DASHBOARD SUMMARY
# =====================================================

def dashboard_summary_service(
    db,
    user
):

    return repo.get_dashboard_summary(
        db
    )


# =====================================================
# TASK DISTRIBUTION
# =====================================================

def task_distribution_service(
    db,
    user
):

    return repo.get_task_distribution(
        db
    )


# =====================================================
# ROLE DASHBOARD
# =====================================================

def role_dashboard_service(
    db,
    user
):

    if user.role == "employee":

        return repo.employee_dashboard(
            db,
            user.id
        )

    elif user.role == "manager":

        return repo.manager_dashboard(
            db,
            user.id
        )

    return repo.admin_dashboard(db)