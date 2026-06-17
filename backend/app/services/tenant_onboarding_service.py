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
from app.schemas.user import (
    UserCreate
)

from app.schemas.tenant import (
    TenantCreate
)

from app.core.security import hash_password

from app.models.workspace import Workspace



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
# CREATE TENANT AND FIRST ADMIN
# =========================================

def create_tenant_and_admin(
    db: Session,
    tenant_payload: TenantCreate,
    admin_payload: UserCreate,
    create_default_workspace: bool = True
):

    # create tenant
    from app.services.tenant_service import create_tenant

    tenant = create_tenant(db, tenant_payload)

    # create admin user
    user = (
        db.query(
            User
        ).filter(
            User.email == admin_payload.email
        ).first()
    )

    if user:
        raise ValueError("User with this email already exists")

    new_user = User(
        name=admin_payload.name,
        email=admin_payload.email,
        hashed_password=hash_password(admin_payload.password),
        role="admin",
        is_active=True,
        tenant_id=tenant.id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # create default settings if missing
    settings = (
        db.query(TenantCollaborationSettings)
        .filter(TenantCollaborationSettings.tenant_id == tenant.id)
        .first()
    )

    settings_created = False

    if not settings:
        settings = TenantCollaborationSettings(
            tenant_id=tenant.id,
            max_workspaces=10,
            max_channels_per_workspace=50,
            max_workspace_members=500,
            max_storage_mb=1024,
            workspace_enabled=True,
            channel_enabled=True
        )

        db.add(settings)

        settings_created = True

    default_workspace_created = False

    if create_default_workspace:
        ws = Workspace(
            tenant_id=tenant.id,
            name=f"{tenant.name} - General",
            slug=f"{tenant.slug}-general",
            description="Default workspace",
            visibility="PUBLIC",
            created_by=new_user.id
        )

        db.add(ws)
        default_workspace_created = True

    onboarding = TenantOnboarding(
        tenant_id=tenant.id,
        admin_user_id=new_user.id,
        onboarding_status="COMPLETED",
        default_workspace_created=default_workspace_created,
        settings_created=settings_created,
        completed_at=datetime.utcnow()
    )

    db.add(onboarding)
    db.commit()
    db.refresh(onboarding)

    return {
        "tenant": tenant,
        "admin": new_user,
        "onboarding": onboarding
    }


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