# app/schemas/ai_meeting_summary.py

from datetime import datetime
from pydantic import BaseModel


class AiMeetingSummaryBase(BaseModel):
    tenant_id: int | None = None
    meeting_id: int
    summary: str | None = None
    action_items: str | None = None
    risks: str | None = None
    decisions: str | None = None


class AiMeetingSummaryCreate(
    AiMeetingSummaryBase
):
    pass


class AiMeetingSummaryOut(
    AiMeetingSummaryBase
):
    id: int
    generated_at: datetime

    model_config = {
        "from_attributes": True
    }
