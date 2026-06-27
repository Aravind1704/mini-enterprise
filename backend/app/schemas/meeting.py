# app/schemas/meeting.py

from datetime import datetime
from pydantic import BaseModel


class MeetingBase(BaseModel):
    tenant_id: int
    project_id: int
    title: str
    description: str | None = None
    start_time: datetime
    end_time: datetime
    created_by: int
    status: str = "SCHEDULED"


class MeetingCreate(MeetingBase):
    pass


class MeetingUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    status: str | None = None


class MeetingOut(MeetingBase):
    created_at: datetime | None = None
    updated_at: datetime | None = None