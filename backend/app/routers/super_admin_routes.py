from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.core.dependencies import (
    get_current_user,
    require_super_admin
)

from app.models.tenant import Tenant
from app.models.user import User
from app.schemas.super_admin import (
    TenantCreate,
    TenantAdminCreate
)

from app.services.super_admin_service import (
    assign_tenant_admin,
    create_tenant,
    create_tenant_admin,
    get_dashboard,
    get_dashboard
)


from app.schemas.super_admin import (
    TenantAdminAssign
)

router = APIRouter(
    prefix="/super-admin",
    tags=["Super Admin"]
)


@router.post("/tenant")
def create_new_tenant(

    payload: TenantCreate,

    db: Session = Depends(
        get_db
    ),

    current_user = Depends(
        require_super_admin
    )
):

    return create_tenant(
        db,
        payload
    )


@router.post("/tenant-admin")
def create_new_admin(

    payload: TenantAdminCreate,

    db: Session = Depends(
        get_db
    ),

    current_user = Depends(
        require_super_admin
    )
):

    return create_tenant_admin(
        db,
        payload
    )



@router.get("/dashboard")
def dashboard(

    db: Session = Depends(
        get_db
    ),

    current_user=Depends(
        require_super_admin
    )
):

    return get_dashboard(db)


@router.post("/assign-admin")
def assign_admin(

    payload: TenantAdminAssign,

    db: Session = Depends(get_db),

    current_user=Depends(
        require_super_admin
    )
):

    return assign_tenant_admin(

        db,

        payload.tenant_id,

        payload.tenant_admin_id,

        current_user.id
    )
@router.get("/tenants")
def get_tenants(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if user.role != "super_admin":
        raise HTTPException(
            status_code=403,
            detail="Only Super Admin"
        )

    return db.query(Tenant).all()


@router.get("/tenant-admins")
def get_tenant_admins(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if user.role != "super_admin":
        raise HTTPException(
            status_code=403,
            detail="Only Super Admin"
        )

    return (
        db.query(User)
        .filter(User.role == "admin")
        .all()
    )

