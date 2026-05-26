# app/services/notification_service.py
from typing import Optional, List
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)


def _create_notification_record(db: Session, user_id: int, title: str, body: str, action_type: str = None, related_id: Optional[int] = None):
    """
    Internal helper: create a Notification record in DB using lazy import to avoid circular imports.
    """
    if db is None:
        return None

    try:
        # Lazy import to avoid circular import issues
        from app.models.notification import Notification
    except Exception as e:
        logger.debug("Notification model not available: %s", e)
        return None

    n = Notification(
        user_id=user_id,
        title=title,
        body=body,
        action_type=action_type,
        related_id=related_id
    )
    try:
        db.add(n)
        db.commit()
        db.refresh(n)
        return n
    except Exception as e:
        logger.exception("Failed to create notification record: %s", e)
        try:
            db.rollback()
        except Exception:
            pass
        return None


def create_notification(user_id: int, message: str, action_type: str, related_id: Optional[int], db: Session):
    """
    Public API to create a notification record.
    """
    title = action_type or "notification"
    return _create_notification_record(db, user_id, title, message, action_type=action_type, related_id=related_id)


def get_user_notifications(user_id: int, db: Session, unread_only: bool = False) -> List:
    """
    Return list of Notification objects for a user, newest first.
    """
    try:
        from app.models.notification import Notification
    except Exception:
        logger.debug("Notification model not available for querying")
        return []

    query = db.query(Notification).filter(Notification.user_id == user_id)
    if unread_only:
        query = query.filter(Notification.is_read == False)
    return query.order_by(Notification.created_at.desc()).all()


def mark_as_read(notification_id: int, db: Session):
    """
    Mark a notification as read and return the updated object.
    """
    try:
        from app.models.notification import Notification
    except Exception:
        logger.debug("Notification model not available for mark_as_read")
        return None

    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if notification:
        notification.is_read = True
        try:
            db.commit()
            db.refresh(notification)
        except Exception:
            try:
                db.rollback()
            except Exception:
                pass
    return notification


def notify_task_assigned(task_id: int, assigned_to_id: int, assigned_by_name: str, db: Optional[Session] = None):
    """
    Convenience helper to notify a user that a task was assigned to them.
    """
    message = f"Task #{task_id} assigned to you by {assigned_by_name}"
    create_notification(assigned_to_id, message, "task_assigned", task_id, db)


def notify_comment_added(task_id: int, task_title: str, commenter_name: str, assigned_to_id: int, db: Optional[Session] = None):
    """
    Notify the assigned user that a comment was added to a task.
    """
    message = f"{commenter_name} commented on '{task_title}'"
    create_notification(assigned_to_id, message, "comment_added", task_id, db)


def notify_approval_requested(approval_id: int, approver_id: int, requester_name: str, db: Optional[Session] = None):
    """
    Notify an approver that an approval request is pending.
    """
    message = f"Approval request from {requester_name}"
    create_notification(approver_id, message, "approval_requested", approval_id, db)


def notify_user(db: Optional[Session], user_id: int, subject: str, message: str, via: Optional[str] = "in_app"):
    """
    Minimal notify_user helper used by background jobs.
    - db: SQLAlchemy Session (optional; pass None if not available)
    - user_id: recipient user id
    - subject: short subject/title
    - message: body text
    - via: 'in_app' | 'email' | 'both'
    Returns True on best-effort success, False otherwise.
    """
    success = False

    # In-app notification (best-effort)
    if via in (None, "in_app", "both"):
        try:
            created = _create_notification_record(db, user_id, subject, message, action_type="system")
            success = success or (created is not None)
        except Exception:
            logger.exception("In-app notification failed for user %s", user_id)

    # Email notification (optional): lazy import and best-effort send
    if via in ("email", "both"):
        try:
            # Lazy import of an email helper if available
            from app.services.email_service import send_email  # optional module
            # send_email should be implemented elsewhere; call best-effort
            send_email(to_user_id=user_id, subject=subject, body=message)
            success = True
        except Exception:
            logger.debug("Email service not available or failed for user %s", user_id)

    return success
