from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text
)

from sqlalchemy.sql import func

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.database import Base


class ApprovalEscalation(Base):

    __tablename__ = "approval_escalations"

    
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    

    approval_id: Mapped[int] = mapped_column(
        ForeignKey("approvals.id"),
        nullable=False
    )

    

    escalated_from: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    escalated_to: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    

    reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    escalation_level: Mapped[int] = mapped_column(
        Integer,
        default=1
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="pending"
    )  # pending / resolved / cancelled

    

    escalated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )