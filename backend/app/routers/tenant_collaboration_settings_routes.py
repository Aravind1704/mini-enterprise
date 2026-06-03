from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.tenant_collaboration_settings import (
    TenantCollaborationSettingsUpdate
)

from app.services.tenant_collaboration_settings_service import (
    get_collaboration_settings,
    update_collaboration_settings
)

router = APIRouter(
    prefix="/tenants",
    tags=["Tenant Collaboration Settings"]
)


@router.get(
    "/{tenant_id}/collaboration/settings"
)
def get_settings(
    tenant_id: int,
    db: Session = Depends(get_db)
):

    return get_collaboration_settings(
        db,
        tenant_id
    )


@router.put(
    "/{tenant_id}/collaboration/settings"
)
def update_settings(
    tenant_id: int,
    payload: TenantCollaborationSettingsUpdate,
    db: Session = Depends(get_db)
):

    return update_collaboration_settings(
        db,
        tenant_id,
        payload
    )