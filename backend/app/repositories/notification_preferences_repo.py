from sqlalchemy.orm import Session
from typing import Optional
from app.models.notification_preferences import NotificationPreferences

class NotificationPreferencesRepo:
    @staticmethod
    def get_by_user(db: Session, user_id: int) -> Optional[NotificationPreferences]:
        return db.query(NotificationPreferences).filter(NotificationPreferences.user_id == user_id).first()

    @staticmethod
    def create_default(db: Session, user_id: int) -> NotificationPreferences:
        prefs = NotificationPreferences(user_id=user_id)
        db.add(prefs)
        db.commit()
        db.refresh(prefs)
        return prefs

    @staticmethod
    def save(db: Session, prefs: NotificationPreferences) -> NotificationPreferences:
        db.add(prefs)
        db.commit()
        db.refresh(prefs)
        return prefs
