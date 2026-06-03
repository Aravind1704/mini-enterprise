from datetime import datetime

from sqlalchemy import (
    Integer,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from sqlalchemy.sql import func

from app.database import Base


class TenantCollaborationUsage(Base):

    __tablename__ = (
        "tenant_collaboration_usage"
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    tenant_id: Mapped[int] = mapped_column(
        ForeignKey("tenants.id"),
        nullable=False
    )

    workspace_count: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    channel_count: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    member_count: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    storage_used_mb: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    last_calculated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )