from sqlalchemy.orm import Session

from app.models.meeting_note import MeetingNote

from app.repositories.meeting_note_repo import (
    MeetingNoteRepo
)


def create_note(
    db: Session,
    meeting_id: int,
    notes: str,
    user_id: int,
    tenant_id: int | None = None
):
    note = MeetingNote(
        tenant_id=tenant_id,
        meeting_id=meeting_id,
        notes=notes,
        created_by=user_id
    )

    return MeetingNoteRepo.create(
        db,
        note
    )


def list_notes(
    db: Session,
    meeting_id: int
):
    return (
        MeetingNoteRepo.list(
            db,
            meeting_id
        )
    )


def update_note(
    db: Session,
    note_id: int,
    notes: str
):
    note = MeetingNoteRepo.get(
        db,
        note_id
    )

    if not note:
        raise ValueError("Note not found")

    note.notes = notes

    return MeetingNoteRepo.save(
        db,
        note
    )
