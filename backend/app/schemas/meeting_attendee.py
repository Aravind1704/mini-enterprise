# app/schemas/meeting_attendee.py

from pydantic import BaseModel


class MeetingAttendeeBase(BaseModel):
    tenant_id: int | None = None
    meeting_id: int
    user_id: int
    attendance_status: str = "INVITED"


class MeetingAttendeeCreate(MeetingAttendeeBase):
    pass


class MeetingAttendeeUpdate(BaseModel):
    attendance_status: str


class MeetingAttendeeOut(MeetingAttendeeBase):
    id: int

    model_config = {
        "from_attributes": True
    }
