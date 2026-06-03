# app/services/tenant_collaboration_settings_service.py

from sqlalchemy.orm import Session

from app.models.tenant import Tenant

from app.models.tenant_collaboration_settings import (
    TenantCollaborationSettings
)

from app.repositories.tenant_repo import (
    TenantRepo
)

from app.repositories.tenant_collaboration_settings_repo import (
    TenantCollaborationSettingsRepo
)

from app.schemas.tenant_collaboration_settings import (
    TenantCollaborationSettingsCreate,
    TenantCollaborationSettingsUpdate
)


# =========================================
# CREATE DEFAULT SETTINGS
# =========================================

def create_default_settings(
    db: Session,
    tenant_id: int
):

    tenant = TenantRepo.get_by_id(
        db,
        tenant_id
    )

    if not tenant:

        raise ValueError(
            "Tenant not found"
        )

    existing = (
        TenantCollaborationSettingsRepo
        .get_by_tenant(
            db,
            tenant_id
        )
    )

    if existing:

        return existing

    settings = (
        TenantCollaborationSettings(
            tenant_id=tenant_id,

            max_workspaces=10,

            max_channels_per_workspace=50,

            max_workspace_members=500,

            max_storage_mb=1024,

            workspace_enabled=True,

            channel_enabled=True
        )
    )

    return (
        TenantCollaborationSettingsRepo
        .create(
            db,
            settings
        )
    )


# =========================================
# GET SETTINGS
# =========================================

def get_collaboration_settings(
    db: Session,
    tenant_id: int
):

    return (
        TenantCollaborationSettingsRepo
        .get_by_tenant(
            db,
            tenant_id
        )
    )


# =========================================
# UPDATE SETTINGS
# =========================================

def update_collaboration_settings(
    db: Session,
    tenant_id: int,
    payload: TenantCollaborationSettingsUpdate
):

    settings = (
        TenantCollaborationSettingsRepo
        .get_by_tenant(
            db,
            tenant_id
        )
    )

    if not settings:

        raise ValueError(
            "Settings not found"
        )

    update_data = payload.dict(
        exclude_unset=True
    )

    for key, value in update_data.items():

        setattr(
            settings,
            key,
            value
        )

    return (
        TenantCollaborationSettingsRepo
        .save(
            db,
            settings
        )
    )


# =========================================
# VALIDATE WORKSPACE LIMIT
# =========================================

def validate_workspace_limit(
    settings,
    current_workspace_count: int
):

    if (
        current_workspace_count
        >= settings.max_workspaces
    ):

        raise ValueError(
            "Maximum workspace limit reached"
        )

    return True


# =========================================
# VALIDATE CHANNEL LIMIT
# =========================================

def validate_channel_limit(
    settings,
    current_channel_count: int
):

    if (
        current_channel_count
        >= settings.max_channels_per_workspace
    ):

        raise ValueError(
            "Maximum channel limit reached"
        )

    return True


# =========================================
# VALIDATE MEMBER LIMIT
# =========================================

def validate_member_limit(
    settings,
    current_member_count: int
):

    if (
        current_member_count
        >= settings.max_workspace_members
    ):

        raise ValueError(
            "Maximum member limit reached"
        )

    return True


# =========================================
# CHECK WORKSPACE FEATURE
# =========================================

def check_workspace_enabled(
    settings
):

    if not settings.workspace_enabled:

        raise ValueError(
            "Workspace module disabled"
        )

    return True


# =========================================
# CHECK CHANNEL FEATURE
# =========================================

def check_channel_enabled(
    settings
):

    if not settings.channel_enabled:

        raise ValueError(
            "Channel module disabled"
        )

    return True