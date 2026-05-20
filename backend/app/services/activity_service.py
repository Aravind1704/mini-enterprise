from sqlalchemy.orm import Session

from app.models.audit import AuditLog


def track_activity(
    db: Session,
    user_id: int,
    action: str,
    entity: str,
    entity_id: int,
    details: str
):

    log = AuditLog(
        user_id=user_id,
        action=action,
        entity=entity,
        entity_id=entity_id,
        details=details
    )

    db.add(log)

    db.commit()

    db.refresh(log)

    return log