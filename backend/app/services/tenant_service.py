# app/services/tenant_service.py

from sqlalchemy.orm import Session
from app.models.tenant import Tenant
from app.core.slug import make_slug

from app.schemas.tenant import (
    TenantCreate,
    TenantUpdate
)

from app.repositories.tenant_repo import (
    TenantRepo
)


# =========================================
# CREATE TENANT
# =========================================

def create_tenant(
    db: Session,
    payload: TenantCreate
) -> Tenant:

    base_slug = make_slug(payload.name)

    slug = base_slug

    idx = 1

    while TenantRepo.get_by_slug(db, slug):
        slug = f"{base_slug}-{idx}"
        idx += 1

    existing_email = (
        TenantRepo.get_by_email(
            db,
            payload.contact_email
        )
    )

    if existing_email:
        raise ValueError(
            "Tenant email already exists"
        )

    tenant = Tenant(
        name=payload.name,
        slug=slug,
        contact_email=payload.contact_email,
        phone=payload.phone,
        address=payload.address,
        industry=payload.industry,
        status="ACTIVE"
    )

    return TenantRepo.create(
        db,
        tenant
    )


# =========================================
# LIST TENANTS
# =========================================

def list_tenants(
    db: Session
):

    return TenantRepo.list_all(
        db
    )


# =========================================
# GET TENANT
# =========================================

def get_tenant(
    db: Session,
    tenant_id: int
):

    return TenantRepo.get_by_id(
        db,
        tenant_id
    )


# =========================================
# GET TENANT BY SLUG
# =========================================

def get_tenant_by_slug(
    db: Session,
    slug: str
):

    return TenantRepo.get_by_slug(
        db,
        slug
    )


# =========================================
# GET TENANT BY EMAIL
# =========================================

def get_tenant_by_email(
    db: Session,
    email: str
):

    return TenantRepo.get_by_email(
        db,
        email
    )


# =========================================
# UPDATE TENANT
# =========================================

def update_tenant(
    db: Session,
    tenant: Tenant,
    payload: TenantUpdate
):

    update_data = payload.dict(
        exclude_unset=True
    )

    if (
        "contact_email" in update_data
        and update_data["contact_email"]
    ):

        existing_email = (
            TenantRepo.get_by_email(
                db,
                update_data["contact_email"]
            )
        )

        if existing_email and existing_email.id != tenant.id:

            raise ValueError(
                "Tenant email already exists"
            )

    if (
        "name" in update_data
        and update_data["name"]
    ):
        base_slug = make_slug(update_data["name"])

        slug = base_slug

        idx = 1

        existing = TenantRepo.get_by_slug(db, slug)

        while existing and existing.id != tenant.id:
            slug = f"{base_slug}-{idx}"
            idx += 1
            existing = TenantRepo.get_by_slug(db, slug)

        tenant.slug = slug

    for key, value in update_data.items():

        setattr(
            tenant,
            key,
            value
        )

    return TenantRepo.save(
        db,
        tenant
    )


# =========================================
# ACTIVATE TENANT
# =========================================

def activate_tenant(
    db: Session,
    tenant: Tenant
):

    tenant.status = "ACTIVE"

    return TenantRepo.save(
        db,
        tenant
    )


# =========================================
# SUSPEND TENANT
# =========================================

def suspend_tenant(
    db: Session,
    tenant: Tenant
):

    tenant.status = "SUSPENDED"

    return TenantRepo.save(
        db,
        tenant
    )


# =========================================
# DELETE TENANT
# =========================================

def delete_tenant(
    db: Session,
    tenant: Tenant
):

    TenantRepo.delete(
        db,
        tenant
    )

    return {
        "message":
        "Tenant deleted successfully"
    }
