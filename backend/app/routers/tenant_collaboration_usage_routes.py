# app/routes/tenant_collaboration_usage_routes.py

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.services.tenant_collaboration_usage_service import (
    get_collaboration_usage,
    recalculate_usage
)

router = APIRouter(
    prefix="/tenants",
    tags=[
        "Tenant Collaboration Usage"
    ]
)


# =========================================
# VIEW USAGE
# =========================================

@router.get(
    "/{tenant_id}/collaboration/usage"
)
def api_get_usage(
    tenant_id: int,
    db: Session = Depends(get_db)
):

    usage = (
        get_collaboration_usage(
            db,
            tenant_id
        )
    )

    if not usage:

        raise HTTPException(
            status_code=404,
            detail="Usage record not found"
        )

    return usage


# =========================================
# RECALCULATE USAGE
# =========================================

@router.post(
    "/{tenant_id}/collaboration/recalculate-usage"
)
def api_recalculate_usage(
    tenant_id: int,
    db: Session = Depends(get_db)
):

    return recalculate_usage(
        db,
        tenant_id
    )