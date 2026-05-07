from sqlalchemy.orm import Session
from app.models.audit import AuditLog
from datetime import datetime, timedelta

def log_action(user_id: int, action: str, entity: str, entity_id: int, details: str, db: Session):
    audit = AuditLog(
        user_id=user_id,
        action=action,
        entity=entity,
        entity_id=entity_id,
        details=details
    )
    db.add(audit)
    db.commit()
    return audit

def get_audit_logs(db: Session, limit: int = 100):
    return db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(limit).all()

def get_user_audit_logs(user_id: int, db: Session, limit: int = 50):
    return db.query(AuditLog).filter(AuditLog.user_id == user_id).order_by(AuditLog.timestamp.desc()).limit(limit).all()

def get_recent_activity(days: int = 7, db: Session = None):
    since = datetime.utcnow() - timedelta(days=days)
    return db.query(AuditLog).filter(AuditLog.timestamp >= since).order_by(AuditLog.timestamp.desc()).all()