import os
import shutil

from sqlalchemy.orm import Session

from app.models.document import Document

UPLOAD_DIR = "uploads"


def upload_document(
    file,
    task_id,
    user_id,
    db: Session
):

    os.makedirs(
        UPLOAD_DIR,
        exist_ok=True
    )

    latest = db.query(Document).filter(
        Document.task_id == task_id
    ).order_by(
        Document.version.desc()
    ).first()

    version = 1

    if latest:
        version = latest.version + 1

    file_path = f"{UPLOAD_DIR}/v{version}_{file.filename}"

    with open(file_path, "wb") as buffer:

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




def get_all_documents(
    db: Session
):

    return db.query(Document).order_by(
        Document.created_at.desc()
    ).all()