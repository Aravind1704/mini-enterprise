from datetime import datetime

from sqlalchemy.orm import Session

from app.models.Team import Team
from app.repositories.team_repo import TeamRepo


def _ensure_team_timestamps(team: Team | None) -> Team | None:
    if not team:
        return team

    now = datetime.utcnow()
    if team.created_at is None:
        team.created_at = now
    if team.updated_at is None:
        team.updated_at = team.created_at or now
    return team


def create_team(
    db: Session,
    payload
):
    team = Team(
        tenant_id=payload.tenant_id,
        workspace_id=payload.workspace_id,
        name=payload.name,
        description=payload.description,
        created_by=payload.created_by,
        is_active=payload.is_active,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    return TeamRepo.create(
        db,
        team
    )


def update_team(
    db: Session,
    team: Team,
    payload
):
    update_data = payload.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(team, key, value)

    team.updated_at = datetime.utcnow()

    return TeamRepo.save(
        db,
        team
    )


def get_team(
    db: Session,
    team_id: int
):
    return _ensure_team_timestamps(TeamRepo.get(
        db,
        team_id
    ))


def list_teams(
    db: Session,
    tenant_id: int,
    workspace_id: int | None = None
):
    return [
        _ensure_team_timestamps(team)
        for team in TeamRepo.list(
            db,
            tenant_id,
            workspace_id
        )
    ]


def delete_team(
    db: Session,
    team_id: int
):
    team = TeamRepo.get(
        db,
        team_id
    )

    if not team:
        raise ValueError(
            "Team not found"
        )

    TeamRepo.delete(
        db,
        team
    )

    return {
        "message":
        "Team deleted successfully"
    }


def archive_team(
    db: Session,
    team: Team
):
    team.is_active = False
    team.updated_at = datetime.utcnow()

    return TeamRepo.save(
        db,
        team
    )


def restore_team(
    db: Session,
    team: Team
):
    team.is_active = True
    team.updated_at = datetime.utcnow()

    return TeamRepo.save(
        db,
        team
    )
