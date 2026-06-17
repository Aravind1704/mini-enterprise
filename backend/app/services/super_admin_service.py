from sqlalchemy.orm import Session

from app.models.tenant import Tenant
from app.models.user import User


from app.core.security import hash_password


def create_tenant(db: Session, payload):

    tenant = Tenant(
        name=payload.name,
        slug=payload.slug,
        contact_email=payload.contact_email,
        phone=payload.phone,
        address=payload.address,
        industry=payload.industry
    )

    db.add(tenant)
    db.commit()
    db.refresh(tenant)

    return tenant


def create_tenant_admin(db: Session, payload):

    admin = User(
        name=payload.name,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role="tenant_admin",
        tenant_id=payload.tenant_id,
        is_active=True
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    return admin



def get_dashboard(db: Session):

    return {
        "total_tenants": db.query(Tenant).count(),
        "total_users": db.query(User).count(),
        "tenant_admins": db.query(User)
            .filter(User.role == "tenant_admin")
            .count()
    }


def get_all_tenants(db: Session):
    return db.query(Tenant).all()


def get_all_tenant_admins(db: Session):
    return (
        db.query(User)
        .filter(User.role == "tenant_admin")
        .all()
    )