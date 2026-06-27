from fastapi import HTTPException, status

from sqlalchemy.orm import Session

from app.models.Team import Team
from app.models.meeting import Meeting
from app.models.project import Project
from app.models.workspace import Workspace
from app.models.user import User


def _bypass(user: User | None) -> bool:
    return bool(user and user.role in {"admin", "super_admin"})


def require_workspace_access(
    db: Session,
    workspace_id: int,
    current_user: User | None = None
) -> Workspace:
    workspace = (
        db.query(Workspace)
        .filter(Workspace.id == workspace_id)
        .first()
    )

    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found"
        )

    if current_user and not _bypass(current_user):
        if current_user.tenant_id != workspace.tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Workspace access denied"
            )

    return workspace


def require_project_access(
    db: Session,
    project_id: int,
    current_user: User | None = None
) -> Project:
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    if current_user and not _bypass(current_user):
        if current_user.tenant_id != project.tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Project access denied"
            )

    return project


def require_team_access(
    db: Session,
    team_id: int,
    current_user: User | None = None
) -> Team:
    team = (
        db.query(Team)
        .filter(Team.id == team_id)
        .first()
    )

    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found"
        )

    if current_user and not _bypass(current_user):
        if current_user.tenant_id != team.tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Team access denied"
            )

    return team


def require_meeting_access(
    db: Session,
    meeting_id: int,
    current_user: User | None = None
) -> Meeting:
    meeting = (
        db.query(Meeting)
        .filter(Meeting.id == meeting_id)
        .first()
    )

    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found"
        )

    if current_user and not _bypass(current_user):
        if current_user.tenant_id != meeting.tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Meeting access denied"
            )

    return meeting
