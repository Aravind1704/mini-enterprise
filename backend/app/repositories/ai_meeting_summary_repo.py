from sqlalchemy.orm import Session

from app.models.ai_meeting_summary import (
    AiMeetingSummary
)


class AiMeetingSummaryRepo:

    @staticmethod
    def create(
        db: Session,
        summary: AiMeetingSummary
    ):
        db.add(summary)
        db.commit()
        db.refresh(summary)
        return summary

    @staticmethod
    def get_by_meeting(
        db: Session,
        meeting_id: int
    ):
        return (
            db.query(AiMeetingSummary)
            .filter(
                AiMeetingSummary.meeting_id == meeting_id
            )
            .first()
        )

    @staticmethod
    def save(
        db: Session,
        summary: AiMeetingSummary
    ):
        db.commit()
        db.refresh(summary)
        return summary