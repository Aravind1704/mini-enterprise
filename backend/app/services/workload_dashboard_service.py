from datetime import datetime

from sqlalchemy import case, func
from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.Team import Team
from app.models.user import User


def user_workload(
    db: Session
):
    rows = (
        db.query(
            Task.assigned_to_id,
            func.count(Task.id),
            func.sum(case((Task.status == "DONE", 1), else_=0)),
            func.sum(case((Task.status.in_(["TODO", "IN_PROGRESS"]), 1), else_=0)),
            func.sum(case((Task.due_date < datetime.utcnow(), 1), else_=0))
        )
        .group_by(Task.assigned_to_id)
        .all()
    )

    results = []
    for user_id, total, completed, pending, overdue in rows:
        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
            if user_id
            else None
        )
        results.append(
            {
                "user_id": user_id,
                "user_name": user.name if user else "Unassigned",
                "total_tasks": int(total or 0),
                "completed_tasks": int(completed or 0),
                "pending_tasks": int(pending or 0),
                "overdue_tasks": int(overdue or 0),
            }
        )

    return results


def team_workload(
    db: Session
):
    rows = (
        db.query(
            Task.team_id,
            func.count(Task.id),
            func.sum(case((Task.status == "DONE", 1), else_=0)),
            func.sum(case((Task.status.in_(["TODO", "IN_PROGRESS"]), 1), else_=0)),
            func.sum(case((Task.due_date < datetime.utcnow(), 1), else_=0))
        )
        .group_by(Task.team_id)
        .all()
    )

    results = []
    for team_id, total, completed, pending, overdue in rows:
        team = (
            db.query(Team)
            .filter(Team.id == team_id)
            .first()
            if team_id
            else None
        )
        results.append(
            {
                "team_id": team_id,
                "team_name": team.name if team else "Unassigned",
                "total_tasks": int(total or 0),
                "completed_tasks": int(completed or 0),
                "pending_tasks": int(pending or 0),
                "overdue_tasks": int(overdue or 0),
            }
        )

    return results


def project_workload(
    db: Session
):
    rows = (
        db.query(
            Task.project_id,
            func.count(Task.id),
            func.sum(case((Task.status == "DONE", 1), else_=0)),
            func.sum(case((Task.status.in_(["TODO", "IN_PROGRESS"]), 1), else_=0)),
            func.sum(case((Task.due_date < datetime.utcnow(), 1), else_=0))
        )
        .group_by(Task.project_id)
        .all()
    )

    return [
        {
            "project_id": project_id,
            "total_tasks": int(total or 0),
            "completed_tasks": int(completed or 0),
            "pending_tasks": int(pending or 0),
            "overdue_tasks": int(overdue or 0),
        }
        for project_id, total, completed, pending, overdue in rows
    ]
