from datetime import datetime

from sqlalchemy import (
    Integer,
    Boolean,
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


class TenantOnboarding(Base):

    __tablename__ = "tenant_onboarding"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    tenant_id: Mapped[int] = mapped_column(
        ForeignKey("tenants.id"),
        nullable=False
    )

    admin_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    onboarding_status: Mapped[str] = mapped_column(
        String(50),
        default="PENDING"
    )

    default_workspace_created: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    settings_created: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )