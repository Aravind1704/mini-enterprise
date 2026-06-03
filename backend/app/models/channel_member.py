from datetime import datetime

from sqlalchemy import (
    Integer,
    Boolean,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from sqlalchemy.sql import func

from app.database import Base


class ChannelMember(Base):

    __tablename__ = "channel_members"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    channel_id: Mapped[int] = mapped_column(
        ForeignKey("channels.id"),
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    joined_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    is_muted: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    last_read_message_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )