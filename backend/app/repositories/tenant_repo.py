from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.tenant import Tenant


class TenantRepo:

    @staticmethod
    def create(
        db: Session,
        tenant: Tenant
    ):

        db.add(tenant)

        db.commit()

        db.refresh(tenant)

        return tenant

    @staticmethod
    def get_by_id(
        db: Session,
        tenant_id: int
    ):

        return db.get(
            Tenant,
            tenant_id
        )

    @staticmethod
    def get_by_slug(
        db: Session,
        slug: str
    ):

        stmt = select(
            Tenant
        ).where(
            Tenant.slug == slug
        )

        return (
            db.execute(stmt)
            .scalars()
            .first()
        )

    @staticmethod
    def get_by_email(
        db: Session,
        email: str
    ):

        stmt = select(
            Tenant
        ).where(
            Tenant.contact_email == email
        )

        return (
            db.execute(stmt)
            .scalars()
            .first()
        )

    @staticmethod
    def list_all(
        db: Session
    ):

        stmt = (
            select(Tenant)
            .order_by(
                Tenant.id.desc()
            )
        )

        return (
            db.execute(stmt)
            .scalars()
            .all()
        )

    @staticmethod
    def save(
        db: Session,
        tenant: Tenant
    ):

        db.add(tenant)

        db.commit()

        db.refresh(tenant)

        return tenant

    @staticmethod
    def delete(
        db: Session,
        tenant: Tenant
    ):

        db.delete(tenant)

        db.commit()