from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.dependencies import get_current_user
from app.services.notification_service import get_user_notifications, mark_as_read

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("/")
def list_notifications(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_user_notifications(current_user.id, db)

@router.get("/unread")
def unread_count(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    unread = get_user_notifications(current_user.id, db, unread_only=True)
    return {"unread_count": len(unread)}

@router.patch("/{id}/read")
def read_notification(id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return mark_as_read(id, db)