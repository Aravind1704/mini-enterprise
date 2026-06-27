from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import get_current_user
from app.core.enterprise_access import require_meeting_access
from app.repositories.meeting_note_repo import MeetingNoteRepo
from app.schemas.meeting_note import MeetingNoteOut, MeetingNoteUpdate
from app.services.meeting_note_service import update_note

router = APIRouter(tags=["Meeting Notes"])


@router.put("/meeting-notes/{note_id}", response_model=MeetingNoteOut)
def api_update_meeting_note(
    note_id: int,
    payload: MeetingNoteUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    note = MeetingNoteRepo.get(db, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    require_meeting_access(db, note.meeting_id, current_user)
    try:
        return update_note(db, note_id, payload.notes)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
