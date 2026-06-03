from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
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


class WorkspaceMember(Base):

    __tablename__ = "workspace_members"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    workspace_id: Mapped[int] = mapped_column(
        ForeignKey("workspaces.id"),
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    role: Mapped[str] = mapped_column(
        String(50),
        default="MEMBER"
    )

    joined_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )