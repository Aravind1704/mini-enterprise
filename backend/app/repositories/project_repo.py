from sqlalchemy.orm import Session

from app.models.project import Project


class ProjectRepo:

    @staticmethod
    def create(
        db: Session,
        project: Project
    ):
        db.add(project)
        db.commit()
        db.refresh(project)
        return project

    @staticmethod
    def get(
        db: Session,
        project_id: int
    ):
        return (
            db.query(Project)
            .filter(
                Project.id == project_id
            )
            .first()
        )

    @staticmethod
    def list(
        db: Session,
        tenant_id: int,
        workspace_id: int | None = None
    ):
        query = db.query(Project).filter(Project.tenant_id == tenant_id)

        if workspace_id is not None:
            query = query.filter(Project.workspace_id == workspace_id)

        return query.all()

    @staticmethod
    def save(
        db: Session,
        project: Project
    ):
        db.commit()
        db.refresh(project)
        return project

    @staticmethod
    def delete(
        db: Session,
        project: Project
    ):
        db.delete(project)
        db.commit()
