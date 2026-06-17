from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from sqlalchemy.sql import func

from app.database import Base


class SuperAdminActivity(Base):

    __tablename__ = "super_admin_activities"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    super_admin_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    action_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    entity_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    entity_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )