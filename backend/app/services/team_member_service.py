from datetime import datetime

from sqlalchemy.orm import Session

from app.models.team_member import TeamMember
from app.repositories.team_repo import TeamRepo
from app.repositories.team_member_repo import (
    TeamMemberRepo
)


def _ensure_team_member_timestamps(member: TeamMember | None) -> TeamMember | None:
    if not member:
        return member

    if member.joined_at is None:
        member.joined_at = datetime.utcnow()
    return member


def add_team_member(
    db: Session,
    team_id: int,
    user_id: int,
    role: str,
    tenant_id: int | None = None
):
    team = TeamRepo.get(
        db,
        team_id
    )

    if not team:
        raise ValueError("Team not found")

    existing = (
        TeamMemberRepo.get_member(
            db,
            team_id,
            user_id
        )
    )

    if existing:
        existing.role = role
        existing.is_active = True
        existing.tenant_id = tenant_id or team.tenant_id
        existing.joined_at = existing.joined_at or datetime.utcnow()

        return TeamMemberRepo.save(
            db,
            existing
        )

    member = TeamMember(
        tenant_id=tenant_id or team.tenant_id,
        team_id=team_id,
        user_id=user_id,
        role=role,
        is_active=True,
        joined_at=datetime.utcnow(),
    )

    return TeamMemberRepo.create(
        db,
        member
    )


def list_team_members(
    db: Session,
    team_id: int
):
    return [
        _ensure_team_member_timestamps(member)
        for member in TeamMemberRepo.list_members(
            db,
            team_id
        )
    ]


def remove_team_member(
    db: Session,
    team_id: int,
    user_id: int
):
    member = (
        TeamMemberRepo.get_member(
            db,
            team_id,
            user_id
        )
    )

    if not member:
        raise ValueError(
            "Member not found"
        )

    member.is_active = False

    TeamMemberRepo.save(
        db,
        member
    )

    return {
        "message":
        "Member removed"
    }
