"""
AI Repository - Phase 4
Database queries for AI service
"""

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from app.models.task import Task
from app.models.approval import Approval


def list_all_tasks(db: Session):
    """List all tasks for admin/global view"""
    try:
        stmt = (
            select(Task)
            .options(
                selectinload(Task.assignee),
                selectinload(Task.creator)
            )
        )
        result = db.execute(stmt)
        return result.scalars().all()
    except Exception as e:
        print(f"Error in list_all_tasks: {e}")
        return []


def list_tasks_for_employee(db: Session, user_id: int):
    """List tasks assigned to a specific employee"""
    try:
        stmt = (
            select(Task)
            .where(Task.assigned_to_id == user_id)
            .options(
                selectinload(Task.assignee),
                selectinload(Task.creator)
            )
        )
        result = db.execute(stmt)
        return result.scalars().all()
    except Exception as e:
        print(f"Error in list_tasks_for_employee: {e}")
        return []


def list_tasks_for_manager(db: Session, user_id: int):
    """List tasks created by or assigned to a manager"""
    try:
        stmt = (
            select(Task)
            .where(
                (Task.created_by_id == user_id)
                | (Task.assigned_to_id == user_id)
            )
            .options(
                selectinload(Task.assignee),
                selectinload(Task.creator)
            )
        )
        result = db.execute(stmt)
        return result.scalars().all()
    except Exception as e:
        print(f"Error in list_tasks_for_manager: {e}")
        return []


def list_pending_approvals(db: Session):
    """List all pending approvals"""
    try:
        stmt = (
            select(Approval)
            .where(Approval.status == "pending")
            .options(
                selectinload(Approval.requester)
            )
        )
        result = db.execute(stmt)
        return result.scalars().all()
    except Exception as e:
        print(f"Error in list_pending_approvals: {e}")
        return []


def get_high_priority_tasks(db: Session, user_id: int = None):
    """Get high priority tasks, optionally filtered by user"""
    try:
        stmt = select(Task).where(Task.priority == "high")

        if user_id:
            stmt = stmt.where(Task.assigned_to_id == user_id)

        result = db.execute(stmt)
        return result.scalars().all()
    except Exception as e:
        print(f"Error in get_high_priority_tasks: {e}")
        return []


def get_overdue_tasks(db: Session, user_id: int = None):
    """Get overdue tasks, optionally filtered by user"""
    try:
        from datetime import datetime

        stmt = (
            select(Task)
            .where(
                (Task.due_date < datetime.utcnow())
                & (Task.status != "done")
            )
        )

        if user_id:
            stmt = stmt.where(Task.assigned_to_id == user_id)

        result = db.execute(stmt)
        return result.scalars().all()
    except Exception as e:
        print(f"Error in get_overdue_tasks: {e}")
        return []


def get_task_count_by_status(db: Session, user_id: int = None):
    """Count tasks by status"""
    try:
        statuses = ["todo", "in_progress", "review", "done"]
        counts = {}

        for status in statuses:
            stmt = select(Task).where(Task.status == status)

            if user_id:
                stmt = stmt.where(Task.assigned_to_id == user_id)

            result = db.execute(stmt)
            counts[status] = len(result.scalars().all())

        return counts
    except Exception as e:
        print(f"Error in get_task_count_by_status: {e}")
        return {}


def get_task_count_by_priority(db: Session, user_id: int = None):
    """Count tasks by priority"""
    try:
        priorities = ["high", "medium", "low"]
        counts = {}

        for priority in priorities:
            stmt = select(Task).where(Task.priority == priority)

            if user_id:
                stmt = stmt.where(Task.assigned_to_id == user_id)

            result = db.execute(stmt)
            counts[priority] = len(result.scalars().all())

        return counts
    except Exception as e:
        print(f"Error in get_task_count_by_priority: {e}")
        return {}