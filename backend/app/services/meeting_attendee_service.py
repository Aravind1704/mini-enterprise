from sqlalchemy.orm import Session

from app.models.meeting_attendee import (
    MeetingAttendee
)

from app.repositories.meeting_attendee_repo import (
    MeetingAttendeeRepo
)


def add_attendee(
    db: Session,
    meeting_id: int,
    user_id: int,
    tenant_id: int | None = None
):
    existing = (
        MeetingAttendeeRepo.get(
            db,
            meeting_id,
            user_id
        )
    )

    if existing:
        raise ValueError(
            "User already added"
        )

    attendee = MeetingAttendee(
        tenant_id=tenant_id,
        meeting_id=meeting_id,
        user_id=user_id
    )

    return (
        MeetingAttendeeRepo.create(
            db,
            attendee
        )
    )


def list_attendees(
    db: Session,
    meeting_id: int
):
    return (
        MeetingAttendeeRepo.list(
            db,
            meeting_id
        )
    )


def remove_attendee(
    db: Session,
    meeting_id: int,
    user_id: int
):
    attendee = MeetingAttendeeRepo.get(
        db,
        meeting_id,
        user_id
    )

    if not attendee:
        raise ValueError("Attendee not found")

    MeetingAttendeeRepo.delete(
        db,
        attendee
    )

    return {
        "message": "Attendee removed"
    }
