from sqlalchemy import (
    select
)

from sqlalchemy.orm import (
    Session
)

from app.models.approval import (
    Approval
)


# =====================================================
# LIST ALL APPROVALS
# =====================================================

def list_all_approvals(
    db: Session
):

    stmt = select(Approval)

    result = db.execute(stmt)

    return result.scalars().all()


# =====================================================
# MANAGER APPROVALS
# =====================================================

def list_manager_approvals(
    db: Session
):

    stmt = (
        select(Approval)
        .where(
            Approval.current_level == "manager"
        )
    )

    result = db.execute(stmt)

    return result.scalars().all()


# =====================================================
# EMPLOYEE APPROVALS
# =====================================================

def list_employee_approvals(
    db: Session,
    user_id: int
):

    stmt = (
        select(Approval)
        .where(
            Approval.requested_by == user_id
        )
    )

    result = db.execute(stmt)

    return result.scalars().all()