from sqlalchemy.orm import Session

from app.models.Team import Team


class TeamRepo:

    @staticmethod
    def create(
        db: Session,
        team: Team
    ):
        db.add(team)
        db.commit()
        db.refresh(team)
        return team

    @staticmethod
    def get(
        db: Session,
        team_id: int
    ):
        return (
            db.query(Team)
            .filter(
                Team.id == team_id
            )
            .first()
        )

    @staticmethod
    def list(
        db: Session,
        tenant_id: int,
        workspace_id: int | None = None
    ):
        query = db.query(Team).filter(Team.tenant_id == tenant_id)

        if workspace_id is not None:
            query = query.filter(Team.workspace_id == workspace_id)

        return query.all()

    @staticmethod
    def save(
        db: Session,
        team: Team
    ):
        db.commit()
        db.refresh(team)
        return team

    @staticmethod
    def delete(
        db: Session,
        team: Team
    ):
        db.delete(team)
        db.commit()
