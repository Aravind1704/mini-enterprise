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


class TenantCollaborationSettings(Base):

    __tablename__ = (
        "tenant_collaboration_settings"
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

    max_workspaces: Mapped[int] = mapped_column(
        Integer,
        default=10
    )

    max_channels_per_workspace: Mapped[int] = mapped_column(
        Integer,
        default=50
    )

    max_workspace_members: Mapped[int] = mapped_column(
        Integer,
        default=500
    )

    max_storage_mb: Mapped[int] = mapped_column(
        Integer,
        default=1024
    )

    workspace_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    channel_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )