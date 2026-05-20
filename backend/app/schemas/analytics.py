from pydantic import (
    BaseModel
)


# =====================================================
# ANALYTICS SUMMARY
# =====================================================

class AnalyticsSummary(
    BaseModel
):

    total_tasks: int

    completed_tasks: int

    pending_tasks: int

    total_users: int

    pending_approvals: int


# =====================================================
# TASK STATUS ANALYTICS
# =====================================================

class TaskStatusAnalytics(
    BaseModel
):

    status: str

    count: int


# =====================================================
# USER TASK ANALYTICS
# =====================================================

class UserTaskAnalytics(
    BaseModel
):

    user_name: str

    task_count: int