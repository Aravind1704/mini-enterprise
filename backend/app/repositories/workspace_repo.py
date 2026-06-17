from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.workspace import Workspace


class WorkspaceRepo:

    @staticmethod
    def create(
        db: Session,
        workspace: Workspace
    ):
        db.add(workspace)
        db.commit()
        db.refresh(workspace)
        return workspace

    @staticmethod
    def get(
        db: Session,
        workspace_id: int
    ):
        return db.get(
            Workspace,
            workspace_id
        )

    @staticmethod
    def list_by_tenant(
        db: Session,
        tenant_id: int
    ):
        stmt = (
            select(Workspace)
            .where(
                Workspace.tenant_id == tenant_id
            )
        )

        return (
            db.execute(stmt)
            .scalars()
            .all()
        )

    @staticmethod
    def list_all(
        db: Session
    ):
        stmt = select(Workspace)
        return (
            db.execute(stmt)
            .scalars()
            .all()
        )

    @staticmethod
    def save(
        db: Session,
        workspace: Workspace
    ):
        db.add(workspace)
        db.commit()
        db.refresh(workspace)
        return workspace