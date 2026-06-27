# app/schemas/project_team.py

from datetime import datetime
from pydantic import BaseModel


class ProjectTeamBase(BaseModel):
    tenant_id: int | None = None
    project_id: int
    team_id: int


class ProjectTeamCreate(ProjectTeamBase):
    pass


class ProjectTeamOut(ProjectTeamBase):
    id: int
    assigned_at: datetime

    model_config = {
        "from_attributes": True
    }
