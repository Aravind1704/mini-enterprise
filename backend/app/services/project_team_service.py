from datetime import datetime

from sqlalchemy.orm import Session

from app.models.project_team import ProjectTeam
from app.repositories.project_team_repo import (
    ProjectTeamRepo
)


def _ensure_project_team_timestamps(assignment: ProjectTeam | None) -> ProjectTeam | None:
    if not assignment:
        return assignment

    if assignment.assigned_at is None:
        assignment.assigned_at = datetime.utcnow()
    return assignment


def assign_team_to_project(
    db: Session,
    project_id: int,
    team_id: int,
    tenant_id: int | None = None
):
    existing = (
        ProjectTeamRepo.get(
            db,
            project_id,
            team_id
        )
    )

    if existing:
        raise ValueError(
            "Team already assigned"
        )

    assignment = ProjectTeam(
        tenant_id=tenant_id,
        project_id=project_id,
        team_id=team_id,
        assigned_at=datetime.utcnow()
    )

    return ProjectTeamRepo.create(
        db,
        assignment
    )


def list_project_teams(
    db: Session,
    project_id: int
):
    return [
        _ensure_project_team_timestamps(assignment)
        for assignment in ProjectTeamRepo.list(
            db,
            project_id
        )
    ]


def remove_project_team(
    db: Session,
    project_id: int,
    team_id: int
):
    assignment = (
        ProjectTeamRepo.get(
            db,
            project_id,
            team_id
        )
    )

    if not assignment:
        raise ValueError(
            "Assignment not found"
        )

    ProjectTeamRepo.delete(
        db,
        assignment
    )

    return {
        "message":
        "Team removed"
    }
