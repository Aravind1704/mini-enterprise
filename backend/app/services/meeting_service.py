from sqlalchemy.orm import Session

from app.models.meeting import Meeting
from app.repositories.meeting_repo import (
    MeetingRepo
)


def create_meeting(
    db: Session,
    payload
):
    meeting = Meeting(
        tenant_id=payload.tenant_id,
        project_id=payload.project_id,
        title=payload.title,
        description=payload.description,
        start_time=payload.start_time,
        end_time=payload.end_time,
        created_by=payload.created_by
    )

    return MeetingRepo.create(
        db,
        meeting
    )


def update_meeting(
    db: Session,
    meeting: Meeting,
    payload
):
    update_data = payload.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(meeting, key, value)

    return MeetingRepo.save(
        db,
        meeting
    )


def get_meeting(
    db: Session,
    meeting_id: int
):
    return MeetingRepo.get(
        db,
        meeting_id
    )


def list_meetings(
    db: Session,
    tenant_id: int,
    project_id: int | None = None
):
    return MeetingRepo.list(
        db,
        tenant_id,
        project_id
    )


def delete_meeting(
    db: Session,
    meeting_id: int
):
    meeting = MeetingRepo.get(
        db,
        meeting_id
    )

    if not meeting:
        raise ValueError(
            "Meeting not found"
        )

    MeetingRepo.delete(
        db,
        meeting
    )

    return {
        "message":
        "Meeting deleted"
    }


def cancel_meeting(
    db: Session,
    meeting: Meeting
):
    meeting.status = "CANCELLED"

    return MeetingRepo.save(
        db,
        meeting
    )


def complete_meeting(
    db: Session,
    meeting: Meeting
):
    meeting.status = "COMPLETED"

    return MeetingRepo.save(
        db,
        meeting
    )
