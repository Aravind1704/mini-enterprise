from sqlalchemy.orm import Session

from app.models.meeting import Meeting


class MeetingRepo:

    @staticmethod
    def create(
        db: Session,
        meeting: Meeting
    ):
        db.add(meeting)
        db.commit()
        db.refresh(meeting)
        return meeting

    @staticmethod
    def get(
        db: Session,
        meeting_id: int
    ):
        return (
            db.query(Meeting)
            .filter(
                Meeting.id == meeting_id
            )
            .first()
        )

    @staticmethod
    def list(
        db: Session,
        tenant_id: int,
        project_id: int | None = None
    ):
        query = db.query(Meeting).filter(Meeting.tenant_id == tenant_id)

        if project_id is not None:
            query = query.filter(Meeting.project_id == project_id)

        return query.all()

    @staticmethod
    def save(
        db: Session,
        meeting: Meeting
    ):
        db.commit()
        db.refresh(meeting)
        return meeting

    @staticmethod
    def delete(
        db: Session,
        meeting: Meeting
    ):
        db.delete(meeting)
        db.commit()
