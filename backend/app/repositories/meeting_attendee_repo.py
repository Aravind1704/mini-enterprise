from sqlalchemy.orm import Session

from app.models.meeting_attendee import (
    MeetingAttendee
)


class MeetingAttendeeRepo:

    @staticmethod
    def create(
        db: Session,
        attendee: MeetingAttendee
    ):
        db.add(attendee)
        db.commit()
        db.refresh(attendee)
        return attendee

    @staticmethod
    def get(
        db: Session,
        meeting_id: int,
        user_id: int
    ):
        return (
            db.query(MeetingAttendee)
            .filter(
                MeetingAttendee.meeting_id == meeting_id,
                MeetingAttendee.user_id == user_id
            )
            .first()
        )

    @staticmethod
    def list(
        db: Session,
        meeting_id: int
    ):
        return (
            db.query(MeetingAttendee)
            .filter(
                MeetingAttendee.meeting_id == meeting_id
            )
            .all()
        )

    @staticmethod
    def delete(
        db: Session,
        attendee: MeetingAttendee
    ):
        db.delete(attendee)
        db.commit()

    @staticmethod
    def save(
        db: Session,
        attendee: MeetingAttendee
    ):
        db.commit()
        db.refresh(attendee)
        return attendee
