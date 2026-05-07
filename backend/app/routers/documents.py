from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.dependencies import get_current_user
from app.services.document_service import upload_document, get_task_documents

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/upload")
def upload_doc(file: UploadFile = File(...), task_id: int = None, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return upload_document(file, task_id, current_user.id, db)

@router.get("/task/{task_id}")
def get_docs(task_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return get_task_documents(task_id, db)