from sqlalchemy.orm import Session
from app.models.notification import Notification

def create_notification(user_id: int, message: str, action_type: str, related_id: int, db: Session):
    notification = Notification(
        user_id=user_id,
        message=message,
        action_type=action_type,
        related_id=related_id
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification

def get_user_notifications(user_id: int, db: Session, unread_only: bool = False):
    query = db.query(Notification).filter(Notification.user_id == user_id)
    if unread_only:
        query = query.filter(Notification.is_read == False)
    return query.order_by(Notification.created_at.desc()).all()

def mark_as_read(notification_id: int, db: Session):
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if notification:
        notification.is_read = True
        db.commit()
        db.refresh(notification)
    return notification

def notify_task_assigned(task_id: int, assigned_to_id: int, assigned_by_name: str, db: Session):
    message = f"Task #{task_id} assigned to you by {assigned_by_name}"
    create_notification(assigned_to_id, message, "task_assigned", task_id, db)

def notify_comment_added(task_id: int, task_title: str, commenter_name: str, assigned_to_id: int, db: Session):
    message = f"{commenter_name} commented on '{task_title}'"
    create_notification(assigned_to_id, message, "comment_added", task_id, db)

def notify_approval_requested(approval_id: int, approver_id: int, requester_name: str, db: Session):
    message = f"Approval request from {requester_name}"
    create_notification(approver_id, message, "approval_requested", approval_id, db)