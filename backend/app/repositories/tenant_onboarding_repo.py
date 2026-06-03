# app/repositories/tenant_onboarding_repo.py

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.tenant_onboarding import (
    TenantOnboarding
)


class TenantOnboardingRepo:

    @staticmethod
    def create(
        db: Session,
        onboarding: TenantOnboarding
    ):

        db.add(onboarding)

        db.commit()

        db.refresh(onboarding)

        return onboarding

    @staticmethod
    def get(
        db: Session,
        onboarding_id: int
    ):

        stmt = select(
            TenantOnboarding
        ).where(
            TenantOnboarding.id == onboarding_id
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

        stmt = select(
            TenantOnboarding
        ).where(
            TenantOnboarding.tenant_id == tenant_id
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
            select(TenantOnboarding)
            .order_by(
                TenantOnboarding.id.desc()
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
        onboarding: TenantOnboarding
    ):

        db.add(onboarding)

        db.commit()

        db.refresh(onboarding)

        return onboarding