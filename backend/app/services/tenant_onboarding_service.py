# app/services/tenant_onboarding_service.py

from datetime import datetime

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.tenant import Tenant

from app.models.tenant_onboarding import (
    TenantOnboarding
)

from app.repositories.tenant_repo import (
    TenantRepo
)

from app.repositories.tenant_onboarding_repo import (
    TenantOnboardingRepo
)

from app.models.tenant_collaboration_settings import (
    TenantCollaborationSettings
)


# =========================================
# CREATE ADMIN FOR EXISTING TENANT
# =========================================

def create_tenant_admin(
    db: Session,
    tenant_id: int,
    admin_user_id: int
):

    tenant = TenantRepo.get_by_id(
        db,
        tenant_id
    )

    if not tenant:

        raise ValueError(
            "Tenant not found"
        )

    user = (
        db.query(User)
        .filter(
            User.id == admin_user_id
        )
        .first()
    )

    if not user:

        raise ValueError(
            "User not found"
        )

    user.tenant_id = tenant.id

    user.role = "ADMIN"

    db.add(user)

    db.commit()

    onboarding = (
        TenantOnboardingRepo
        .get_by_tenant(
            db,
            tenant_id
        )
    )

    if onboarding:

        onboarding.admin_user_id = (
            admin_user_id
        )

        onboarding.onboarding_status = (
            "COMPLETED"
        )

        onboarding.completed_at = (
            datetime.utcnow()
        )

        TenantOnboardingRepo.save(
            db,
            onboarding
        )

    return onboarding


# =========================================
# ONBOARD TENANT
# =========================================

def onboard_tenant(
    db: Session,
    tenant_id: int,
    admin_user_id: int,
    create_default_workspace: bool = True
):

    tenant = TenantRepo.get_by_id(
        db,
        tenant_id
    )

    if not tenant:

        raise ValueError(
            "Tenant not found"
        )

    user = (
        db.query(User)
        .filter(
            User.id == admin_user_id
        )
        .first()
    )

    if not user:

        raise ValueError(
            "Admin user not found"
        )

    user.role = "ADMIN"

    user.tenant_id = tenant.id

    db.add(user)

    settings = (
        db.query(
            TenantCollaborationSettings
        )
        .filter(
            TenantCollaborationSettings
            .tenant_id
            == tenant.id
        )
        .first()
    )

    settings_created = False

    if not settings:

        settings = (
            TenantCollaborationSettings(
                tenant_id=tenant.id,
                max_workspaces=10,
                max_channels_per_workspace=50,
                max_workspace_members=500,
                max_storage_mb=1024,
                workspace_enabled=True,
                channel_enabled=True
            )
        )

        db.add(settings)

        settings_created = True

    onboarding = TenantOnboarding(

        tenant_id=tenant.id,

        admin_user_id=user.id,

        onboarding_status="COMPLETED",

        default_workspace_created=
        create_default_workspace,

        settings_created=
        settings_created,

        completed_at=
        datetime.utcnow()
    )

    db.add(onboarding)

    db.commit()

    db.refresh(onboarding)

    return onboarding


# =========================================
# GET ONBOARDING STATUS
# =========================================

def get_onboarding_status(
    db: Session,
    tenant_id: int
):

    return (
        TenantOnboardingRepo
        .get_by_tenant(
            db,
            tenant_id
        )
    )


# =========================================
# LIST ALL ONBOARDING RECORDS
# =========================================

def list_onboarding_records(
    db: Session
):

    return (
        TenantOnboardingRepo
        .list_all(db)
    )