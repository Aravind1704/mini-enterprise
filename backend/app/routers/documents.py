from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    Form,
    HTTPException
)

from fastapi.responses import FileResponse

from sqlalchemy.orm import Session

import os

from app.database import get_db

from app.core.dependencies import (
    get_current_user
)

from app.models.document import Document
from app.models.task import Task

from app.services.document_service import (
    upload_document,
    get_all_documents
)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


# ----------------------------
# GET ALL DOCUMENTS
# ----------------------------

@router.get("/")
def list_documents(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return get_all_documents(db)


# ----------------------------
# UPLOAD DOCUMENT
# ----------------------------

@router.post("/upload")
def upload(
    task_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return upload_document(
        file=file,
        task_id=task_id,
        user_id=current_user.id,
        db=db
    )


# ----------------------------
# DOWNLOAD DOCUMENT
# ----------------------------

@router.get("/download/{id}")
def download_document(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    document = db.query(Document).filter(
        Document.id == id
    ).first()

    if not document:

        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    if not os.path.exists(document.file_path):

        raise HTTPException(
            status_code=404,
            detail="File not found on server"
        )

    return FileResponse(
        path=document.file_path,
        filename=document.file_name,
        media_type="application/octet-stream"
    )


# ----------------------------
# DELETE DOCUMENT
# ----------------------------

@router.delete("/{id}")
def delete_document(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    document = db.query(Document).filter(
        Document.id == id
    ).first()

    if not document:

        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    # DELETE FILE FROM FOLDER

    if os.path.exists(document.file_path):

        os.remove(document.file_path)

    # DELETE FROM DATABASE

    db.delete(document)

    db.commit()

    return {
        "message": "Document deleted successfully"
    }