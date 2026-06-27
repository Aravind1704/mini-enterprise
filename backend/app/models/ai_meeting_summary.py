from datetime import datetime

from sqlalchemy import (
    Integer,
    Text,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from sqlalchemy.sql import func

from app.database import Base


class AiMeetingSummary(Base):
    __tablename__ = "ai_meeting_summaries"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    tenant_id: Mapped[int | None] = mapped_column(
        ForeignKey("tenants.id"),
        nullable=False
    )

    meeting_id: Mapped[int] = mapped_column(
        ForeignKey("meetings.id"),
        nullable=False
    )

    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    action_items: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    risks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    decisions: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    generated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    tenant = relationship(
        "Tenant"
    )

    meeting = relationship(
        "Meeting",
        back_populates="ai_summaries"
    )
