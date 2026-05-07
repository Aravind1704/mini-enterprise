from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.dependencies import get_current_user
from app.services.ai_service import get_ai_summary

router = APIRouter(prefix="/dashboard", tags=["AI"])

@router.get("/ai-summary")
def ai_summary(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_ai_summary(current_user.id, db)