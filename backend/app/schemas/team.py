# app/schemas/team.py

from datetime import datetime
from pydantic import BaseModel


class TeamBase(BaseModel):
    tenant_id: int
    workspace_id: int
    name: str
    description: str | None = None
    is_active: bool = True


class TeamCreate(TeamBase):
    pass


class TeamUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class TeamOut(TeamBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }