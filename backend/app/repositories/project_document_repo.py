from sqlalchemy.orm import Session

from app.models.project_document import ProjectDocument


class ProjectDocumentRepo:

    @staticmethod
    def create(
        db: Session,
        document: ProjectDocument
    ):
        db.add(document)
        db.commit()
        db.refresh(document)
        return document

    @staticmethod
    def get(
        db: Session,
        document_id: int
    ):
        return (
            db.query(ProjectDocument)
            .filter(
                ProjectDocument.id == document_id
            )
            .first()
        )

    @staticmethod
    def list(
        db: Session,
        project_id: int
    ):
        return (
            db.query(ProjectDocument)
            .filter(
                ProjectDocument.project_id == project_id
            )
            .all()
        )

    @staticmethod
    def delete(
        db: Session,
        document: ProjectDocument
    ):
        db.delete(document)
        db.commit()

    @staticmethod
    def save(
        db: Session,
        document: ProjectDocument
    ):
        db.commit()
        db.refresh(document)
        return document
