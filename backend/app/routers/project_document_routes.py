import os

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import get_current_user
from app.core.enterprise_access import require_project_access
from app.services.project_document_service import (
    delete_project_document,
    get_project_document,
)

router = APIRouter(tags=["Project Documents"])


@router.get("/project-documents/{document_id}/download")
def api_download_project_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    document = get_project_document(db, document_id)
    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    require_project_access(db, document.project_id, current_user)
    if not os.path.exists(document.file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document file missing")
    return FileResponse(
        document.file_path,
        filename=document.file_name,
        media_type=document.mime_type or "application/octet-stream",
    )


@router.delete("/project-documents/{document_id}")
def api_delete_project_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    document = get_project_document(db, document_id)
    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    require_project_access(db, document.project_id, current_user)
    return delete_project_document(db, document)
