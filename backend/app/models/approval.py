from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey
)

from sqlalchemy.sql import func

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.database import Base




class Approval(Base):

    __tablename__ = "approvals"

    

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    

    requested_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    

    status: Mapped[str] = mapped_column(
        String(20),
        default="pending"
    )

    current_level: Mapped[str] = mapped_column(
        String(20),
        default="manager"
    )

    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        onupdate=func.now()
    )




class ApprovalHistory(Base):

    __tablename__ = "approval_history"

    

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    

    approval_id: Mapped[int | None] = mapped_column(
        ForeignKey("approvals.id"),
        nullable=True
    )

    action_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    

    action: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )