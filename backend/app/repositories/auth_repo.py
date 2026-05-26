"""
Audit Repository - Phase 4
Database queries for audit logs
"""

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from app.models.audit import AuditLog


def list_all_logs(db: Session):
    """List all audit logs (admin only)"""
    try:
        stmt = (
            select(AuditLog)
            .options(selectinload(AuditLog.user))
            .order_by(AuditLog.timestamp.desc())
        )
        result = db.execute(stmt)
        return result.scalars().all()
    except Exception as e:
        print(f"Error in list_all_logs: {e}")
        return []


def list_logs_for_employee(db: Session, user_id: int):
    """List audit logs created by a specific user (employee view)"""
    try:
        stmt = (
            select(AuditLog)
            .where(AuditLog.user_id == user_id)
            .options(selectinload(AuditLog.user))
            .order_by(AuditLog.timestamp.desc())
        )
        result = db.execute(stmt)
        return result.scalars().all()
    except Exception as e:
        print(f"Error in list_logs_for_employee: {e}")
        return []


def list_logs_for_manager(db: Session, user_id: int):
    """List audit logs for manager's team"""
    try:
        # Managers see logs for their managed activities
        # This could include team members' actions
        stmt = (
            select(AuditLog)
            .options(selectinload(AuditLog.user))
            .order_by(AuditLog.timestamp.desc())
        )
        result = db.execute(stmt)
        return result.scalars().all()
    except Exception as e:
        print(f"Error in list_logs_for_manager: {e}")
        return []


def list_logs_for_entity(db: Session, entity_type: str, entity_id: int):
    """List all audit logs for a specific entity (task, approval, etc)"""
    try:
        stmt = (
            select(AuditLog)
            .where(
                (AuditLog.entity == entity_type)
                & (AuditLog.entity_id == entity_id)
            )
            .options(selectinload(AuditLog.user))
            .order_by(AuditLog.timestamp.asc())
        )
        result = db.execute(stmt)
        return result.scalars().all()
    except Exception as e:
        print(f"Error in list_logs_for_entity: {e}")
        return []


def create_log(
    db: Session,
    user_id: int,
    action: str,
    entity: str,
    entity_id: int,
    details: str = None
):
    """Create a new audit log entry"""
    try:
        log = AuditLog(
            user_id=user_id,
            action=action,
            entity=entity,
            entity_id=entity_id,
            details=details or ""
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log
    except Exception as e:
        print(f"Error in create_log: {e}")
        db.rollback()
        return None


def get_log_by_id(db: Session, log_id: int):
    """Get a single audit log by ID"""
    try:
        stmt = (
            select(AuditLog)
            .where(AuditLog.id == log_id)
            .options(selectinload(AuditLog.user))
        )
        result = db.execute(stmt)
        return result.scalar_one_or_none()
    except Exception as e:
        print(f"Error in get_log_by_id: {e}")
        return None


def count_logs_for_user(db: Session, user_id: int):
    """Count total logs created by a user"""
    try:
        stmt = select(AuditLog).where(AuditLog.user_id == user_id)
        result = db.execute(stmt)
        logs = result.scalars().all()
        return len(logs)
    except Exception as e:
        print(f"Error in count_logs_for_user: {e}")
        return 0


def count_logs_for_entity(db: Session, entity_type: str, entity_id: int):
    """Count logs for a specific entity"""
    try:
        stmt = select(AuditLog).where(
            (AuditLog.entity == entity_type)
            & (AuditLog.entity_id == entity_id)
        )
        result = db.execute(stmt)
        logs = result.scalars().all()
        return len(logs)
    except Exception as e:
        print(f"Error in count_logs_for_entity: {e}")
        return 0


def get_recent_logs(db: Session, limit: int = 50):
    """Get recent audit logs"""
    try:
        stmt = (
            select(AuditLog)
            .options(selectinload(AuditLog.user))
            .order_by(AuditLog.timestamp.desc())
            .limit(limit)
        )
        result = db.execute(stmt)
        return result.scalars().all()
    except Exception as e:
        print(f"Error in get_recent_logs: {e}")
        return []


def delete_old_logs(db: Session, days: int = 90):
    """Delete audit logs older than specified days"""
    try:
        from datetime import datetime, timedelta

        cutoff_date = datetime.utcnow() - timedelta(days=days)

        stmt = select(AuditLog).where(AuditLog.timestamp < cutoff_date)
        result = db.execute(stmt)
        old_logs = result.scalars().all()

        for log in old_logs:
            db.delete(log)

        db.commit()
        return len(old_logs)

    except Exception as e:
        print(f"Error in delete_old_logs: {e}")
        db.rollback()
        return 0