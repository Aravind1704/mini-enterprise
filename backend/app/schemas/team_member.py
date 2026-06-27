# app/schemas/team_member.py

from datetime import datetime
from pydantic import BaseModel


class TeamMemberBase(BaseModel):
    tenant_id: int | None = None
    team_id: int
    user_id: int
    role: str = "MEMBER"
    is_active: bool = True


class TeamMemberCreate(TeamMemberBase):
    pass


class TeamMemberOut(TeamMemberBase):
    id: int
    joined_at: datetime

    model_config = {
        "from_attributes": True
    }
