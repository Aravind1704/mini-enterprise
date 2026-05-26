import os
import shutil

from sqlalchemy import (
    select
)

from sqlalchemy.orm import (
    Session
)

from app.models.document import (
    Document
)

from app.models.task import (
    Task
)

UPLOAD_DIR = "uploads"


# =====================================================
# LIST ALL DOCUMENTS
# =====================================================

def list_all_documents(
    db: Session
):

    stmt = (
        select(Document)
        .order_by(
            Document.created_at.desc()
        )
    )

    result = db.execute(stmt)

    return result.scalars().all()


# =====================================================
# EMPLOYEE DOCUMENTS
# =====================================================

def list_documents_for_employee(
    db: Session,
    user_id: int
):

    stmt = (
        select(Document)
        .join(Task)
        .where(
            Task.assigned_to_id == user_id
        )
        .order_by(
            Document.created_at.desc()
        )
    )

    result = db.execute(stmt)

    return result.scalars().all()


# =====================================================
# MANAGER DOCUMENTS
# =====================================================

def list_documents_for_manager(
    db: Session,
    user_id: int
):

    stmt = (
        select(Document)
        .order_by(
            Document.created_at.desc()
        )
    )

    result = db.execute(stmt)

    return result.scalars().all()


# =====================================================
# GET TASK
# =====================================================

def get_task_by_id(
    db: Session,
    task_id: int
):

    stmt = (
        select(Task)
        .where(
            Task.id == task_id
        )
    )

    result = db.execute(stmt)

    return result.scalar_one_or_none()


# =====================================================
# CREATE DOCUMENT
# =====================================================

def create_document(
    db: Session,
    file,
    task_id,
    user_id
):

    os.makedirs(
        UPLOAD_DIR,
        exist_ok=True
    )

    latest = (
        db.query(Document)
        .filter(
            Document.task_id == task_id
        )
        .order_by(
            Document.version.desc()
        )
        .first()
    )

    version = 1

    if latest:

        version = latest.version + 1

    file_path = (
        f"{UPLOAD_DIR}/v{version}_{file.filename}"
    )

    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    document = Document(
        file_name=file.filename,
        file_path=file_path,
        version=version,
        uploaded_by=user_id,
        task_id=task_id
    )

    db.add(document)

    db.commit()

    db.refresh(document)

    return document


# =====================================================
# GET DOCUMENT
# =====================================================

def get_document_by_id(
    db: Session,
    document_id: int
):

    stmt = (
        select(Document)
        .where(
            Document.id == document_id
        )
    )

    result = db.execute(stmt)

    return result.scalar_one_or_none()


# =====================================================
# DELETE DOCUMENT
# =====================================================

def delete_document(
    db: Session,
    document
):

    db.delete(document)

    db.commit()