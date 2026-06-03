# app/repositories/channel_member_repo.py

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.channel_member import (
    ChannelMember
)


class ChannelMemberRepo:

    @staticmethod
    def create(
        db: Session,
        member: ChannelMember
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
            select(ChannelMember)
            .where(
                ChannelMember.id == member_id
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
        channel_id: int,
        user_id: int
    ):

        stmt = (
            select(ChannelMember)
            .where(
                ChannelMember.channel_id
                == channel_id,
                ChannelMember.user_id
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
        channel_id: int
    ):

        stmt = (
            select(ChannelMember)
            .where(
                ChannelMember.channel_id
                == channel_id
            )
            .order_by(
                ChannelMember.joined_at.desc()
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
        member: ChannelMember
    ):

        db.add(member)

        db.commit()

        db.refresh(member)

        return member

    @staticmethod
    def delete(
        db: Session,
        member: ChannelMember
    ):

        db.delete(member)

        db.commit()