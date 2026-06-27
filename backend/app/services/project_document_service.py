import os
import uuid

from sqlalchemy.orm import Session

from app.models.project_document import (
    ProjectDocument
)

from app.repositories.project_document_repo import (
    ProjectDocumentRepo
)


UPLOAD_DIR = (
    "uploads/project_documents"
)

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


def upload_project_document(
    db: Session,
    project_id: int,
    file,
    uploaded_by: int,
    tenant_id: int | None = None,
    document_type: str = "OTHER"
):
    safe_name = f"{uuid.uuid4().hex}_{file.filename}"

    path = os.path.join(
        UPLOAD_DIR,
        safe_name
    )

    contents = file.file.read()

    with open(
        path,
        "wb"
    ) as f:
        f.write(contents)

    document = ProjectDocument(
        tenant_id=tenant_id,
        project_id=project_id,
        file_name=file.filename,
        file_path=path,
        file_size=len(contents),
        mime_type=file.content_type,
        uploaded_by=uploaded_by,
        document_type=document_type
    )

    return (
        ProjectDocumentRepo.create(
            db,
            document
        )
    )


def list_project_documents(
    db: Session,
    project_id: int
):
    return (
        ProjectDocumentRepo.list(
            db,
            project_id
        )
    )


def get_project_document(
    db: Session,
    document_id: int
):
    return (
        ProjectDocumentRepo.get(
            db,
            document_id
        )
    )


def delete_project_document(
    db: Session,
    document: ProjectDocument
):
    if os.path.exists(document.file_path):
        os.remove(document.file_path)

    ProjectDocumentRepo.delete(
        db,
        document
    )

    return {
        "message": "Document deleted"
    }
