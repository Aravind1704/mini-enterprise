from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import get_current_user
from app.core.enterprise_access import require_meeting_access, require_project_access
from app.schemas.ai_meeting_summary import AiMeetingSummaryCreate, AiMeetingSummaryOut
from app.schemas.meeting import MeetingCreate, MeetingOut, MeetingUpdate
from app.schemas.meeting_attendee import MeetingAttendeeCreate, MeetingAttendeeOut
from app.schemas.meeting_note import MeetingNoteCreate, MeetingNoteOut, MeetingNoteUpdate
from app.services.ai_meeting_summary_service import create_summary, get_summary
from app.services.meeting_attendee_service import (
    add_attendee,
    list_attendees,
    remove_attendee,
)
from app.services.meeting_note_service import (
    create_note,
    list_notes,
)
from app.services.meeting_service import (
    cancel_meeting,
    complete_meeting,
    create_meeting,
    delete_meeting,
    get_meeting,
    list_meetings,
    update_meeting,
)

router = APIRouter(prefix="/meetings", tags=["Meetings"])


@router.post("/", response_model=MeetingOut, status_code=status.HTTP_201_CREATED)
def api_create_meeting(
    payload: MeetingCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    project = require_project_access(db, payload.project_id, current_user)
    if payload.tenant_id != project.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="tenant_id does not match project",
        )
    request_payload = payload.model_copy(
        update={
            "tenant_id": project.tenant_id,
            "created_by": current_user.id,
        }
    )
    return create_meeting(db, request_payload)


@router.get("/", response_model=list[MeetingOut])
def api_list_meetings(
    tenant_id: int | None = None,
    project_id: int | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if project_id is not None:
        project = require_project_access(db, project_id, current_user)
        tenant_id = project.tenant_id
    if tenant_id is None:
        tenant_id = current_user.tenant_id
    if tenant_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="tenant_id is required",
        )
    return list_meetings(db, tenant_id, project_id)


@router.get("/{meeting_id}", response_model=MeetingOut)
def api_get_meeting(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    meeting = require_meeting_access(db, meeting_id, current_user)
    return meeting


@router.put("/{meeting_id}", response_model=MeetingOut)
def api_update_meeting(
    meeting_id: int,
    payload: MeetingUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    meeting = require_meeting_access(db, meeting_id, current_user)
    return update_meeting(db, meeting, payload)


@router.delete("/{meeting_id}", response_model=MeetingOut)
def api_cancel_meeting(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    meeting = require_meeting_access(db, meeting_id, current_user)
    return cancel_meeting(db, meeting)


@router.patch("/{meeting_id}/complete", response_model=MeetingOut)
def api_complete_meeting(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    meeting = require_meeting_access(db, meeting_id, current_user)
    return complete_meeting(db, meeting)


@router.post("/{meeting_id}/attendees", response_model=MeetingAttendeeOut, status_code=status.HTTP_201_CREATED)
def api_add_attendee(
    meeting_id: int,
    payload: MeetingAttendeeCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    meeting = require_meeting_access(db, meeting_id, current_user)
    if payload.meeting_id != meeting_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="meeting_id does not match path parameter",
        )
    request_payload = payload.model_copy(update={"tenant_id": meeting.tenant_id})
    try:
        return add_attendee(db, meeting_id, request_payload.user_id, request_payload.tenant_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/{meeting_id}/attendees", response_model=list[MeetingAttendeeOut])
def api_list_attendees(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    require_meeting_access(db, meeting_id, current_user)
    return list_attendees(db, meeting_id)


@router.delete("/{meeting_id}/attendees/{user_id}")
def api_remove_attendee(
    meeting_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    require_meeting_access(db, meeting_id, current_user)
    try:
        return remove_attendee(db, meeting_id, user_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.post("/{meeting_id}/notes", response_model=MeetingNoteOut, status_code=status.HTTP_201_CREATED)
def api_add_meeting_note(
    meeting_id: int,
    payload: MeetingNoteCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    meeting = require_meeting_access(db, meeting_id, current_user)
    request_payload = payload.model_copy(
        update={
            "tenant_id": meeting.tenant_id,
            "created_by": current_user.id,
            "meeting_id": meeting_id,
        }
    )
    return create_note(
        db,
        meeting_id,
        request_payload.notes,
        request_payload.created_by,
        request_payload.tenant_id,
    )


@router.get("/{meeting_id}/notes", response_model=list[MeetingNoteOut])
def api_list_meeting_notes(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    require_meeting_access(db, meeting_id, current_user)
    return list_notes(db, meeting_id)


@router.post("/{meeting_id}/summary", response_model=AiMeetingSummaryOut, status_code=status.HTTP_201_CREATED)
def api_generate_summary(
    meeting_id: int,
    payload: AiMeetingSummaryCreate | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    meeting = require_meeting_access(db, meeting_id, current_user)
    request_payload = payload or AiMeetingSummaryCreate(meeting_id=meeting_id)
    return create_summary(
        db,
        meeting_id,
        request_payload.summary or "",
        request_payload.action_items,
        request_payload.risks,
        request_payload.decisions,
        meeting.tenant_id,
    )


@router.get("/{meeting_id}/summary", response_model=AiMeetingSummaryOut)
def api_get_summary(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    require_meeting_access(db, meeting_id, current_user)
    summary = get_summary(db, meeting_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    return summary
