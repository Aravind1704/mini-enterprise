# app/routes/tenant_routes.py

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from typing import List

from app.database import get_db

from app.schemas.tenant import (
    TenantCreate,
    TenantUpdate,
    TenantOut
)

from app.services.tenant_service import (
    create_tenant,
    list_tenants,
    get_tenant,
    update_tenant,
    activate_tenant,
    suspend_tenant,
    delete_tenant
)

router = APIRouter(
    prefix="/tenants",
    tags=["Tenants"]
)


# =========================================
# CREATE TENANT
# =========================================

@router.post(
    "/",
    response_model=TenantOut,
    status_code=status.HTTP_201_CREATED
)
def api_create_tenant(
    payload: TenantCreate,
    db: Session = Depends(get_db)
):

    try:

        return create_tenant(
            db,
            payload
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# =========================================
# LIST TENANTS
# =========================================

@router.get(
    "/",
    response_model=List[TenantOut]
)
def api_list_tenants(
    db: Session = Depends(get_db)
):

    return list_tenants(db)


# =========================================
# GET TENANT
# =========================================

@router.get(
    "/{tenant_id}",
    response_model=TenantOut
)
def api_get_tenant(
    tenant_id: int,
    db: Session = Depends(get_db)
):

    tenant = get_tenant(
        db,
        tenant_id
    )

    if not tenant:

        raise HTTPException(
            status_code=404,
            detail="Tenant not found"
        )

    return tenant


# =========================================
# UPDATE TENANT
# =========================================

@router.put(
    "/{tenant_id}",
    response_model=TenantOut
)
def api_update_tenant(
    tenant_id: int,
    payload: TenantUpdate,
    db: Session = Depends(get_db)
):

    tenant = get_tenant(
        db,
        tenant_id
    )

    if not tenant:

        raise HTTPException(
            status_code=404,
            detail="Tenant not found"
        )

    return update_tenant(
        db,
        tenant,
        payload
    )


# =========================================
# ACTIVATE TENANT
# =========================================

@router.patch(
    "/{tenant_id}/activate",
    response_model=TenantOut
)
def api_activate_tenant(
    tenant_id: int,
    db: Session = Depends(get_db)
):

    tenant = get_tenant(
        db,
        tenant_id
    )

    if not tenant:

        raise HTTPException(
            status_code=404,
            detail="Tenant not found"
        )

    return activate_tenant(
        db,
        tenant
    )


# =========================================
# SUSPEND TENANT
# =========================================

@router.patch(
    "/{tenant_id}/suspend",
    response_model=TenantOut
)
def api_suspend_tenant(
    tenant_id: int,
    db: Session = Depends(get_db)
):

    tenant = get_tenant(
        db,
        tenant_id
    )

    if not tenant:

        raise HTTPException(
            status_code=404,
            detail="Tenant not found"
        )

    return suspend_tenant(
        db,
        tenant
    )


# =========================================
# DELETE TENANT
# =========================================

@router.delete(
    "/{tenant_id}"
)
def api_delete_tenant(
    tenant_id: int,
    db: Session = Depends(get_db)
):

    tenant = get_tenant(
        db,
        tenant_id
    )

    if not tenant:

        raise HTTPException(
            status_code=404,
            detail="Tenant not found"
        )

    return delete_tenant(
        db,
        tenant
    )