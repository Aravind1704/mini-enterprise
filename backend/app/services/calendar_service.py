from datetime import datetime

from sqlalchemy.orm import Session
from app.models.project import Project
from app.models.meeting import Meeting
from app.models.task import Task


def upcoming_meetings(
    db: Session,
    tenant_id: int
):
    return (
        db.query(Meeting)
        .filter(
            Meeting.tenant_id == tenant_id,
            Meeting.status == "SCHEDULED"
        )
        .all()
    )


def upcoming_tasks(
    db: Session,
    tenant_id: int
):
    return (
        db.query(Task)
        .filter(
            Task.tenant_id == tenant_id
        )
        .all()
    )


def project_calendar(
    db: Session,
    project_id: int
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    meetings = (
        db.query(Meeting)
        .filter(
            Meeting.project_id == project_id
        )
        .order_by(Meeting.start_time.asc())
        .all()
    )

    tasks = (
        db.query(Task)
        .filter(
            Task.project_id == project_id
        )
        .all()
    )

    tasks = sorted(
        tasks,
        key=lambda task: (
            task.due_date is None,
            task.due_date or datetime.max,
            task.id,
        ),
    )

    milestones = []
    release_dates = []

    if project:
        if project.start_date:
            milestones.append(
                {
                    "id": f"project-start-{project.id}",
                    "title": f"{project.name} kickoff",
                    "date": project.start_date,
                    "type": "START",
                }
            )

        if project.end_date:
            release_dates.append(
                {
                    "id": f"project-release-{project.id}",
                    "title": f"{project.name} release",
                    "date": project.end_date,
                    "type": "RELEASE",
                }
            )
            milestones.append(
                {
                    "id": f"project-end-{project.id}",
                    "title": f"{project.name} milestone",
                    "date": project.end_date,
                    "type": "MILESTONE",
                }
            )

    return {
        "meetings": [
            {
                "id": meeting.id,
                "title": meeting.title,
                "description": meeting.description,
                "start_time": meeting.start_time,
                "end_time": meeting.end_time,
                "status": meeting.status,
            }
            for meeting in meetings
        ],
        "tasks": [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "due_date": task.due_date,
                "status": task.status,
                "priority": task.priority,
                "team_id": task.team_id,
                "assigned_to_id": task.assigned_to_id,
            }
            for task in tasks
        ],
        "milestones": milestones,
        "release_dates": release_dates,
    }
