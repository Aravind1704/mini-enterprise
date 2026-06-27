from sqlalchemy.orm import Session

from app.models.project_team import ProjectTeam


class ProjectTeamRepo:

    @staticmethod
    def create(
        db: Session,
        project_team: ProjectTeam
    ):
        db.add(project_team)
        db.commit()
        db.refresh(project_team)
        return project_team

    @staticmethod
    def get(
        db: Session,
        project_id: int,
        team_id: int
    ):
        return (
            db.query(ProjectTeam)
            .filter(
                ProjectTeam.project_id == project_id,
                ProjectTeam.team_id == team_id
            )
            .first()
        )

    @staticmethod
    def list(
        db: Session,
        project_id: int
    ):
        return (
            db.query(ProjectTeam)
            .filter(
                ProjectTeam.project_id == project_id
            )
            .all()
        )

    @staticmethod
    def delete(
        db: Session,
        project_team: ProjectTeam
    ):
        db.delete(project_team)
        db.commit()