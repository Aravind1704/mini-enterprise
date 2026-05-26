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

from app.models.user import (
    User
)

from app.models.approval import (
    Approval
)


# =====================================================
# ANALYTICS SUMMARY
# =====================================================

def get_analytics_summary(
    db: Session
):

    total_tasks = db.execute(
        select(func.count(Task.id))
    ).scalar()

    completed_tasks = db.execute(
        select(func.count(Task.id))
        .where(Task.status == "done")
    ).scalar()

    pending_tasks = db.execute(
        select(func.count(Task.id))
        .where(Task.status != "done")
    ).scalar()

    total_users = db.execute(
        select(func.count(User.id))
    ).scalar()

    pending_approvals = db.execute(
        select(func.count(Approval.id))
        .where(Approval.status == "pending")
    ).scalar()

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "total_users": total_users,
        "pending_approvals": pending_approvals
    }


# =====================================================
# TASK STATUS ANALYTICS
# =====================================================

def get_task_status_analytics(
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
# USER TASK ANALYTICS
# =====================================================

def get_user_task_analytics(
    db: Session
):

    stmt = (
        select(
            User.name,
            func.count(Task.id)
        )
        .join(
            Task,
            Task.assigned_to_id == User.id
        )
        .group_by(
            User.name
        )
    )

    result = db.execute(stmt)

    analytics = []

    for row in result:

        analytics.append({

            "user_name": row[0],

            "task_count": row[1]

        })

    return analytics