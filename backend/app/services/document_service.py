from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException
import shutil
import os
from app.models.document import Document
from app.models.audit import AuditLog

UPLOAD_DIR = "uploads"

def upload_document(file: UploadFile, task_id: int, user_id: int, db: Session):
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    
    file_path = f"{UPLOAD_DIR}/{file.filename}"
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=400, detail="File upload failed")
    
    document = Document(
        file_name=file.filename,
        file_path=file_path,
        uploaded_by=user_id,
        task_id=task_id,
        version=1
    )
    db.add(document)
    
    # Log action
    audit = AuditLog(
        user_id=user_id,
        action="uploaded",
        entity="Document",
        entity_id=0,  # Will update after commit
        details=f"Uploaded {file.filename}"
    )
    db.add(audit)
    db.commit()
    db.refresh(document)
    return document

def get_task_documents(task_id: int, db: Session):
    return db.query(Document).filter(Document.task_id == task_id).all()