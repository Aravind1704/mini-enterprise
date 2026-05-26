<<<<<<< HEAD
from sqlalchemy.orm import Session
from typing import Optional

from app.models.audit import AuditLog


class AuditRepo:

    # =====================================================
    # CREATE AUDIT LOG
    # =====================================================

    @staticmethod
    def create(
        db: Session,
        log: AuditLog
    ):

        db.add(log)

        db.commit()

        db.refresh(log)

        return log

    # =====================================================
    # GET ALL LOGS
    # =====================================================

    @staticmethod
    def list_all(
        db: Session
    ):

        return db.query(
            AuditLog
        ).order_by(
            AuditLog.timestamp.desc()
        ).all()

    # =====================================================
    # FILTER LOGS
    # =====================================================

    @staticmethod
    def list(
        db: Session,
        entity: Optional[str] = None,
        user_id: Optional[int] = None
    ):

        q = db.query(AuditLog)

        if entity:

            q = q.filter(
                AuditLog.entity == entity
            )

        if user_id:

            q = q.filter(
                AuditLog.user_id == user_id
            )

        return q.order_by(
            AuditLog.timestamp.desc()
        ).all()
=======
from sqlalchemy import (
    select
)

from sqlalchemy.orm import (
    Session
)

from app.models.audit import (
    AuditLog
)


# =====================================================
# LIST ALL LOGS
# =====================================================

def list_all_logs(
    db: Session
):

    stmt = (
        select(AuditLog)
        .order_by(
            AuditLog.timestamp.desc()
        )
    )

    result = db.execute(stmt)

    return result.scalars().all()
>>>>>>> 4500000c8c54ec045a9125ffb74854e6cb5209d2
