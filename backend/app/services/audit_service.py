from sqlalchemy.orm import Session
from app.models.audit import AuditLog


def log_action(
    db: Session,
    user_id,
    action,
    entity,
    entity_id,
    details
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


def get_audit_logs(db: Session):

    return db.query(AuditLog).order_by(
        AuditLog.timestamp.desc()
    ).all()