from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.services.tenant_onboarding_service import (
    onboard_tenant,
    create_tenant_admin,
    get_onboarding_status
)

router = APIRouter(
    prefix="/tenants",
    tags=["Tenant Onboarding"]
)


@router.post("/onboard")
def api_onboard_tenant(
    tenant_id: int,
    admin_user_id: int,
    db: Session = Depends(get_db)
):

    try:

        return onboard_tenant(
            db,
            tenant_id,
            admin_user_id
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post("/{tenant_id}/admin")
def api_create_admin(
    tenant_id: int,
    admin_user_id: int,
    db: Session = Depends(get_db)
):

    return create_tenant_admin(
        db,
        tenant_id,
        admin_user_id
    )


@router.get("/{tenant_id}/onboarding-status")
def api_get_status(
    tenant_id: int,
    db: Session = Depends(get_db)
):

    return get_onboarding_status(
        db,
        tenant_id
    )