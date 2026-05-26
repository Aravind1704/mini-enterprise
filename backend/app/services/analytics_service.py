from app.repositories import (
    analytics_repo as repo
)


# =====================================================
# ANALYTICS SUMMARY SERVICE
# =====================================================

def analytics_summary_service(
    db,
    user
):

    return repo.get_analytics_summary(
        db
    )


# =====================================================
# TASK STATUS ANALYTICS SERVICE
# =====================================================

def task_status_analytics_service(
    db,
    user
):

    return repo.get_task_status_analytics(
        db
    )


# =====================================================
# USER TASK ANALYTICS SERVICE
# =====================================================

def user_task_analytics_service(
    db,
    user
):

    return repo.get_user_task_analytics(
        db
    )