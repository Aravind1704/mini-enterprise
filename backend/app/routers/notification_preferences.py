from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.notification_preferences import NotificationPreferencesOut, NotificationPreferencesUpdate
from app.services.notification_preferences_service import get_or_create_prefs, update_prefs
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/notification-preferences", tags=["Notification Preferences"])

@router.get("/me", response_model=NotificationPreferencesOut)
def api_get_my_prefs(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    prefs = get_or_create_prefs(db, current_user.id)
    return prefs

@router.put("/me", response_model=NotificationPreferencesOut)
def api_update_my_prefs(payload: NotificationPreferencesUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    prefs = update_prefs(db, current_user.id, payload.dict(exclude_unset=True))
    return prefs

@router.post("/default/{user_id}", response_model=NotificationPreferencesOut)
def api_create_default(user_id: int, db: Session = Depends(get_db)):
    prefs = get_or_create_prefs(db, user_id)
    return prefs
