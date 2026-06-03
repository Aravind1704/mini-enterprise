from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.workspace import Workspace
from app.models.channel import Channel
from app.models.workspace_member import WorkspaceMember
from app.models.tenant_collaboration_usage import (
    TenantCollaborationUsage
)


class TenantCollaborationUsageRepo:

    @staticmethod
    def create(
        db: Session,
        usage: TenantCollaborationUsage
    ):
        db.add(usage)
        db.commit()
        db.refresh(usage)
        return usage

    @staticmethod
    def get_by_tenant(
        db: Session,
        tenant_id: int
    ):
        stmt = (
            select(TenantCollaborationUsage)
            .where(
                TenantCollaborationUsage.tenant_id
                == tenant_id
            )
        )

        return (
            db.execute(stmt)
            .scalars()
            .first()
        )

    @staticmethod
    def get_workspace_count(
        db: Session,
        tenant_id: int
    ):
        stmt = (
            select(
                func.count(Workspace.id)
            )
            .where(
                Workspace.tenant_id
                == tenant_id
            )
        )

        return db.execute(stmt).scalar() or 0

    @staticmethod
    def get_channel_count(
        db: Session,
        tenant_id: int
    ):
        stmt = (
            select(
                func.count(Channel.id)
            )
            .where(
                Channel.tenant_id
                == tenant_id
            )
        )

        return db.execute(stmt).scalar() or 0

    @staticmethod
    def get_member_count(
        db: Session,
        tenant_id: int
    ):
        stmt = (
            select(
                func.count(
                    WorkspaceMember.id
                )
            )
            .join(
                Workspace,
                Workspace.id
                == WorkspaceMember.workspace_id
            )
            .where(
                Workspace.tenant_id
                == tenant_id
            )
        )

        return db.execute(stmt).scalar() or 0

    @staticmethod
    def save(
        db: Session,
        usage: TenantCollaborationUsage
    ):
        db.add(usage)
        db.commit()
        db.refresh(usage)
        return usage