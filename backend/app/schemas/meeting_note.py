# app/schemas/meeting_note.py

from datetime import datetime
from pydantic import BaseModel


class MeetingNoteBase(BaseModel):
    tenant_id: int | None = None
    meeting_id: int
    notes: str
    created_by: int


class MeetingNoteCreate(MeetingNoteBase):
    pass


class MeetingNoteUpdate(BaseModel):
    notes: str


class MeetingNoteOut(MeetingNoteBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
