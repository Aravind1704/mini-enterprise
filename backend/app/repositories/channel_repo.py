# app/repositories/channel_repo.py

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.channel import Channel


class ChannelRepo:

    @staticmethod
    def create(
        db: Session,
        channel: Channel
    ):

        db.add(channel)

        db.commit()

        db.refresh(channel)

        return channel

    @staticmethod
    def get(
        db: Session,
        channel_id: int
    ):

        stmt = (
            select(Channel)
            .where(
                Channel.id == channel_id
            )
        )

        return (
            db.execute(stmt)
            .scalars()
            .first()
        )

    @staticmethod
    def get_by_name(
        db: Session,
        workspace_id: int,
        name: str
    ):

        stmt = (
            select(Channel)
            .where(
                Channel.workspace_id == workspace_id,
                Channel.name == name
            )
        )

        return (
            db.execute(stmt)
            .scalars()
            .first()
        )

    @staticmethod
    def list_by_workspace(
        db: Session,
        workspace_id: int
    ):

        stmt = (
            select(Channel)
            .where(
                Channel.workspace_id
                == workspace_id
            )
            .order_by(
                Channel.created_at.desc()
            )
        )

        return (
            db.execute(stmt)
            .scalars()
            .all()
        )

    @staticmethod
    def list_active_by_workspace(
        db: Session,
        workspace_id: int
    ):

        stmt = (
            select(Channel)
            .where(
                Channel.workspace_id
                == workspace_id,
                Channel.is_archived == False
            )
            .order_by(
                Channel.created_at.desc()
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
        channel: Channel
    ):

        db.add(channel)

        db.commit()

        db.refresh(channel)

        return channel

    @staticmethod
    def delete(
        db: Session,
        channel: Channel
    ):

        db.delete(channel)

        db.commit()