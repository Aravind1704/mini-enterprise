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

def list_all_approvals(db: Session, tenant_id: int | None = None):

    stmt = select(Approval)
    if tenant_id is not None:
        stmt = stmt.where(Approval.tenant_id == tenant_id)

    result = db.execute(stmt)

    return result.scalars().all()


# =====================================================
# MANAGER APPROVALS
# =====================================================

def list_manager_approvals(db: Session, tenant_id: int | None = None):

    filters = [Approval.current_level == "manager"]
    if tenant_id is not None:
        filters.append(Approval.tenant_id == tenant_id)

    stmt = select(Approval).where(*filters)

    result = db.execute(stmt)

    return result.scalars().all()


# =====================================================
# EMPLOYEE APPROVALS
# =====================================================

def list_employee_approvals(
    db: Session,
    user_id: int,
    tenant_id: int | None = None
):

    filters = [Approval.requested_by == user_id]
    if tenant_id is not None:
        filters.append(Approval.tenant_id == tenant_id)

    stmt = select(Approval).where(*filters)

    result = db.execute(stmt)

    return result.scalars().all()
