# app/schemas/project.py

from datetime import datetime, date
from pydantic import BaseModel


class ProjectBase(BaseModel):
    tenant_id: int
    workspace_id: int
    owner_id: int
    name: str
    description: str | None = None
    status: str = "PLANNED"
    priority: str = "MEDIUM"
    start_date: date | None = None
    end_date: date | None = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    owner_id: int | None = None
    status: str | None = None
    priority: str | None = None
    start_date: date | None = None
    end_date: date | None = None


class ProjectOut(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
