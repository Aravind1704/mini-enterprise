"""
AI Service - Phase 4
AI-powered dashboard summary and insights
"""

from datetime import datetime
from typing import Dict, List, Any

from app.repositories import ai_repo as repo


def get_ai_summary_service(db, user) -> Dict[str, Any]:
    """
    Generate AI summary based on user role and tasks.
    Returns aggregated insights about tasks, approvals, and deadlines.
    """

    try:
        # Get tasks based on user role
        if user.role == "employee":
            tasks = repo.list_tasks_for_employee(db, user.id)
        elif user.role == "manager":
            tasks = repo.list_tasks_for_manager(db, user.id)
        else:  # admin
            tasks = repo.list_all_tasks(db)

        # Get pending approvals
        approvals = repo.list_pending_approvals(db)

        # Analyze tasks
        high_priority = [
            task for task in tasks
            if hasattr(task, 'priority') and task.priority == "high"
        ]

        pending = [
            task for task in tasks
            if hasattr(task, 'status') and task.status == "todo"
        ]

        in_progress = [
            task for task in tasks
            if hasattr(task, 'status') and task.status == "in_progress"
        ]

        overdue = [
            task for task in tasks
            if (
                hasattr(task, 'due_date')
                and task.due_date
                and task.due_date < datetime.utcnow()
                and hasattr(task, 'status')
                and task.status != "done"
            )
        ]

        # Generate summary
        summary_text = generate_summary(
            high_priority=high_priority,
            pending=pending,
            in_progress=in_progress,
            overdue=overdue,
            approvals=approvals,
            user_role=user.role
        )

        return {
            "total_tasks": len(tasks) if tasks else 0,
            "high_priority_tasks": len(high_priority),
            "pending_tasks": len(pending),
            "in_progress_tasks": len(in_progress),
            "overdue_tasks": len(overdue),
            "pending_approvals": len(approvals) if approvals else 0,
            "summary": summary_text,
            "role": user.role,
            "generated_at": datetime.utcnow().isoformat()
        }

    except Exception as e:
        # Return safe fallback response
        return {
            "total_tasks": 0,
            "high_priority_tasks": 0,
            "pending_tasks": 0,
            "in_progress_tasks": 0,
            "overdue_tasks": 0,
            "pending_approvals": 0,
            "summary": "Unable to generate AI summary",
            "role": user.role,
            "error": str(e),
            "generated_at": datetime.utcnow().isoformat()
        }


def generate_summary(
    high_priority: List,
    pending: List,
    in_progress: List,
    overdue: List,
    approvals: List,
    user_role: str
) -> str:
    """
    Generate natural language summary of task status and recommendations.
    """

    messages = []

    # High priority messages
    if high_priority:
        messages.append(
            f"⚠️ {len(high_priority)} high priority task{'s' if len(high_priority) > 1 else ''} need immediate attention"
        )
    else:
        messages.append("✅ No high priority tasks")

    # Pending messages
    if pending:
        messages.append(
            f"📋 {len(pending)} task{'s' if len(pending) > 1 else ''} waiting to be started"
        )
    else:
        messages.append("✅ No pending tasks")

    # In progress messages
    if in_progress:
        messages.append(
            f"🔄 {len(in_progress)} task{'s' if len(in_progress) > 1 else ''} currently in progress"
        )

    # Overdue messages
    if overdue:
        messages.append(
            f"🚨 {len(overdue)} OVERDUE task{'s' if len(overdue) > 1 else ''} - action required"
        )

    # Approval messages (for managers and admins)
    if user_role in ["manager", "admin"] and approvals:
        messages.append(
            f"📝 {len(approvals)} approval{'s' if len(approvals) > 1 else ''} waiting for review"
        )

    # Default message if everything is good
    if not messages:
        messages.append("✨ All systems nominal! Keep up the great work!")

    return " | ".join(messages)


def get_task_insights(tasks: List) -> Dict[str, Any]:
    """
    Analyze tasks and return insights.
    """

    if not tasks:
        return {
            "total": 0,
            "by_status": {},
            "by_priority": {},
            "insights": []
        }

    by_status = {}
    by_priority = {}

    for task in tasks:
        # Count by status
        status = getattr(task, 'status', 'unknown')
        by_status[status] = by_status.get(status, 0) + 1

        # Count by priority
        priority = getattr(task, 'priority', 'medium')
        by_priority[priority] = by_priority.get(priority, 0) + 1

    insights = []

    # Generate insights
    if by_priority.get('high', 0) > 0:
        insights.append("High priority tasks need attention")

    if by_status.get('todo', 0) > by_status.get('done', 0):
        insights.append("More tasks to do than completed")

    if by_status.get('done', 0) > 0:
        completion_rate = (by_status.get('done', 0) / len(tasks)) * 100
        if completion_rate > 70:
            insights.append("Good progress on task completion")

    return {
        "total": len(tasks),
        "by_status": by_status,
        "by_priority": by_priority,
        "insights": insights if insights else ["All systems normal"]
    }


def get_productivity_score(user, db) -> Dict[str, Any]:
    """
    Calculate productivity score for a user based on completed tasks.
    """

    try:
        from app.models.task import Task
        from sqlalchemy import select

        # Get completed tasks this week
        stmt = select(Task).where(
            (Task.assigned_to_id == user.id) &
            (Task.status == "done")
        )
        result = db.execute(stmt)
        completed = len(result.scalars().all())

        # Get total tasks this week
        stmt = select(Task).where(Task.assigned_to_id == user.id)
        result = db.execute(stmt)
        total = len(result.scalars().all())

        score = (completed / total * 100) if total > 0 else 0

        return {
            "score": round(score, 2),
            "completed": completed,
            "total": total,
            "percentage": f"{round(score)}%"
        }

    except Exception as e:
        return {
            "score": 0,
            "completed": 0,
            "total": 0,
            "percentage": "0%",
            "error": str(e)
        }