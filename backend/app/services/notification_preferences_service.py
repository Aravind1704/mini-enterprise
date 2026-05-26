# app/services/notification_preferences_service.py
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.notification_preferences import NotificationPreferences
from app.repositories.notification_preferences_repo import NotificationPreferencesRepo
from app.repositories.audit_repo import AuditRepo
from app.models.audit import AuditLog

def get_or_create_prefs(db: Session, user_id: int) -> NotificationPreferences:
    """
    Return existing NotificationPreferences for a user or create defaults.
    """
    prefs = NotificationPreferencesRepo.get_by_user(db, user_id)
    if not prefs:
        prefs = NotificationPreferencesRepo.create_default(db, user_id)
    return prefs


def update_prefs(db: Session, user_id: int, payload: Dict[str, Any]) -> NotificationPreferences:
    """
    Update a user's notification preferences.
    - payload: dict of fields to update (only keys that exist on the model are applied)
    """
    prefs = NotificationPreferencesRepo.get_by_user(db, user_id)
    if not prefs:
        prefs = NotificationPreferencesRepo.create_default(db, user_id)

    for k, v in payload.items():
        if hasattr(prefs, k):
            setattr(prefs, k, v)

    prefs = NotificationPreferencesRepo.save(db, prefs)

    # Audit the change
    try:
        AuditRepo.create(db, AuditLog(
            user_id=user_id,
            module_name="notification_preferences",
            action_type="preferences_updated",
            record_id=prefs.id,
            details="Updated notification preferences"
        ))
    except Exception:
        # Do not fail the update if audit logging fails; rollback DB session if needed
        try:
            db.rollback()
        except Exception:
            pass

    return prefs
