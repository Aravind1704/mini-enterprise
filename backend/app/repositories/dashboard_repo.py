from sqlalchemy import (
    select,
    func
)

from sqlalchemy.orm import (
    Session
)

from app.models.task import (
    Task
)

from app.models.approval import (
    Approval
)

from app.models.user import (
    User
)


# =====================================================
# DASHBOARD SUMMARY
# =====================================================

def get_dashboard_summary(
    db: Session
):

    total_tasks = db.execute(
        select(func.count(Task.id))
    ).scalar()

    todo = db.execute(
        select(func.count(Task.id))
        .where(Task.status == "todo")
    ).scalar()

    in_progress = db.execute(
        select(func.count(Task.id))
        .where(Task.status == "in_progress")
    ).scalar()

    review = db.execute(
        select(func.count(Task.id))
        .where(Task.status == "review")
    ).scalar()

    done = db.execute(
        select(func.count(Task.id))
        .where(Task.status == "done")
    ).scalar()

    pending_approvals = db.execute(
        select(func.count(Approval.id))
        .where(Approval.status == "pending")
    ).scalar()

    return {
        "total_tasks": total_tasks,
        "todo": todo,
        "in_progress": in_progress,
        "review": review,
        "done": done,
        "pending_approvals": pending_approvals
    }


# =====================================================
# TASK DISTRIBUTION
# =====================================================

def get_task_distribution(
    db: Session
):

    return [

        {
            "status": "todo",
            "count": db.execute(
                select(func.count(Task.id))
                .where(Task.status == "todo")
            ).scalar()
        },

        {
            "status": "in_progress",
            "count": db.execute(
                select(func.count(Task.id))
                .where(Task.status == "in_progress")
            ).scalar()
        },

        {
            "status": "review",
            "count": db.execute(
                select(func.count(Task.id))
                .where(Task.status == "review")
            ).scalar()
        },

        {
            "status": "done",
            "count": db.execute(
                select(func.count(Task.id))
                .where(Task.status == "done")
            ).scalar()
        }

    ]


# =====================================================
# EMPLOYEE DASHBOARD
# =====================================================

def employee_dashboard(
    db: Session,
    user_id: int
):

    my_tasks = db.execute(
        select(func.count(Task.id))
        .where(
            Task.assigned_to_id == user_id
        )
    ).scalar()

    pending_tasks = db.execute(
        select(func.count(Task.id))
        .where(
            Task.assigned_to_id == user_id,
            Task.status != "done"
        )
    ).scalar()

    return {
        "role": "employee",
        "my_tasks": my_tasks,
        "pending_tasks": pending_tasks
    }


# =====================================================
# MANAGER DASHBOARD
# =====================================================

def manager_dashboard(
    db: Session,
    user_id: int
):

    team_tasks = db.execute(
        select(func.count(Task.id))
    ).scalar()

    pending_approvals = db.execute(
        select(func.count(Approval.id))
        .where(
            Approval.status == "pending"
        )
    ).scalar()

    return {
        "role": "manager",
        "team_tasks": team_tasks,
        "pending_approvals": pending_approvals
    }


# =====================================================
# ADMIN DASHBOARD
# =====================================================

def admin_dashboard(
    db: Session
):

    total_users = db.execute(
        select(func.count(User.id))
    ).scalar()

    total_tasks = db.execute(
        select(func.count(Task.id))
    ).scalar()

    total_approvals = db.execute(
        select(func.count(Approval.id))
    ).scalar()

    return {
        "role": "admin",
        "total_users": total_users,
        "total_tasks": total_tasks,
        "total_approvals": total_approvals
    }