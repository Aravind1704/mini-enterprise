from sqlalchemy.orm import Session

from app.models.meeting_note import MeetingNote


class MeetingNoteRepo:

    @staticmethod
    def create(
        db: Session,
        note: MeetingNote
    ):
        db.add(note)
        db.commit()
        db.refresh(note)
        return note

    @staticmethod
    def get(
        db: Session,
        note_id: int
    ):
        return (
            db.query(MeetingNote)
            .filter(
                MeetingNote.id == note_id
            )
            .first()
        )

    @staticmethod
    def list(
        db: Session,
        meeting_id: int
    ):
        return (
            db.query(MeetingNote)
            .filter(
                MeetingNote.meeting_id == meeting_id
            )
            .all()
        )

    @staticmethod
    def save(
        db: Session,
        note: MeetingNote
    ):
        db.commit()
        db.refresh(note)
        return note