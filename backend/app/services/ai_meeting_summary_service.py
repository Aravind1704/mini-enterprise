from sqlalchemy.orm import Session

from app.models.ai_meeting_summary import (
    AiMeetingSummary
)

from app.repositories.ai_meeting_summary_repo import (
    AiMeetingSummaryRepo
)
from app.repositories.meeting_note_repo import MeetingNoteRepo


def create_summary(
    db: Session,
    meeting_id: int,
    summary: str,
    action_items: str = None,
    risks: str = None,
    decisions: str = None,
    tenant_id: int | None = None
):
    if not summary:
        notes = MeetingNoteRepo.list(
            db,
            meeting_id
        )
        notes_blob = "\n".join(
            note.notes for note in notes
        )
        summary = "AI summary placeholder based on meeting notes."
        if notes_blob:
            summary = f"{summary}\n{notes_blob}"

    existing = AiMeetingSummaryRepo.get_by_meeting(
        db,
        meeting_id
    )

    if existing:
        existing.tenant_id = tenant_id or existing.tenant_id
        existing.summary = summary
        existing.action_items = action_items
        existing.risks = risks
        existing.decisions = decisions

        return AiMeetingSummaryRepo.save(
            db,
            existing
        )

    ai = AiMeetingSummary(
        tenant_id=tenant_id,
        meeting_id=meeting_id,
        summary=summary,
        action_items=action_items,
        risks=risks,
        decisions=decisions
    )

    return (
        AiMeetingSummaryRepo.create(
            db,
            ai
        )
    )


def get_summary(
    db: Session,
    meeting_id: int
):
    return (
        AiMeetingSummaryRepo.get_by_meeting(
            db,
            meeting_id
        )
    )
