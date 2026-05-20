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