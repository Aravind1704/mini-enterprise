# app/repositories/workspace_member_repo.py

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.workspace_member import (
    WorkspaceMember
)


class WorkspaceMemberRepo:

    @staticmethod
    def create(
        db: Session,
        member: WorkspaceMember
    ):

        db.add(member)

        db.commit()

        db.refresh(member)

        return member

    @staticmethod
    def get(
        db: Session,
        member_id: int
    ):

        stmt = (
            select(WorkspaceMember)
            .where(
                WorkspaceMember.id
                == member_id
            )
        )

        return (
            db.execute(stmt)
            .scalars()
            .first()
        )

    @staticmethod
    def get_member(
        db: Session,
        workspace_id: int,
        user_id: int
    ):

        stmt = (
            select(WorkspaceMember)
            .where(
                WorkspaceMember.workspace_id
                == workspace_id,
                WorkspaceMember.user_id
                == user_id
            )
        )

        return (
            db.execute(stmt)
            .scalars()
            .first()
        )

    @staticmethod
    def list_members(
        db: Session,
        workspace_id: int
    ):

        stmt = (
            select(WorkspaceMember)
            .where(
                WorkspaceMember.workspace_id
                == workspace_id
            )
            .order_by(
                WorkspaceMember.joined_at.desc()
            )
        )

        return (
            db.execute(stmt)
            .scalars()
            .all()
        )

    @staticmethod
    def search_members(
        db: Session,
        workspace_id: int,
        user_id: int
    ):

        stmt = (
            select(WorkspaceMember)
            .where(
                WorkspaceMember.workspace_id
                == workspace_id,
                WorkspaceMember.user_id
                == user_id
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
        member: WorkspaceMember
    ):

        db.add(member)

        db.commit()

        db.refresh(member)

        return member

    @staticmethod
    def delete(
        db: Session,
        member: WorkspaceMember
    ):

        db.delete(member)

        db.commit()