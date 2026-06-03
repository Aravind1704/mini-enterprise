# app/repositories/tenant_collaboration_settings_repo.py

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.tenant_collaboration_settings import (
    TenantCollaborationSettings
)


class TenantCollaborationSettingsRepo:

    @staticmethod
    def create(
        db: Session,
        settings: TenantCollaborationSettings
    ):

        db.add(settings)

        db.commit()

        db.refresh(settings)

        return settings

    @staticmethod
    def get(
        db: Session,
        settings_id: int
    ):

        stmt = (
            select(
                TenantCollaborationSettings
            )
            .where(
                TenantCollaborationSettings.id
                == settings_id
            )
        )

        return (
            db.execute(stmt)
            .scalars()
            .first()
        )

    @staticmethod
    def get_by_tenant(
        db: Session,
        tenant_id: int
    ):

        stmt = (
            select(
                TenantCollaborationSettings
            )
            .where(
                TenantCollaborationSettings.tenant_id
                == tenant_id
            )
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
            select(
                TenantCollaborationSettings
            )
            .order_by(
                TenantCollaborationSettings.id.desc()
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
        settings: TenantCollaborationSettings
    ):

        db.add(settings)

        db.commit()

        db.refresh(settings)

        return settings

    @staticmethod
    def delete(
        db: Session,
        settings: TenantCollaborationSettings
    ):

        db.delete(settings)

        db.commit()