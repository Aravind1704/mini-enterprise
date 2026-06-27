# app/models/task.py

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Integer,
    String,
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

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.project import Project
    from app.models.Team import Team
    from app.models.channel import Channel
    from app.models.workspace import Workspace
    from app.models.tenant import Tenant


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    tenant_id: Mapped[int | None] = mapped_column(
        ForeignKey("tenants.id"),
        nullable=True
    )

    workspace_id: Mapped[int | None] = mapped_column(
        ForeignKey("workspaces.id"),
        nullable=True
    )

    channel_id: Mapped[int | None] = mapped_column(
        ForeignKey("channels.id"),
        nullable=True
    )

    project_id: Mapped[int | None] = mapped_column(
        ForeignKey("projects.id"),
        nullable=True
    )

    team_id: Mapped[int | None] = mapped_column(
        ForeignKey("teams.id"),
        nullable=True
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="TODO"
    )

    priority: Mapped[str] = mapped_column(
        String(20),
        default="MEDIUM"
    )

    due_date: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    created_by_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    assigned_to_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    updated_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    # =========================
    # User Relationships
    # =========================

    creator: Mapped["User"] = relationship(
        "User",
        foreign_keys=[created_by_id]
    )

    assignee: Mapped["User"] = relationship(
        "User",
        foreign_keys=[assigned_to_id]
    )

    updater: Mapped["User"] = relationship(
        "User",
        foreign_keys=[updated_by]
    )

    # =========================
    # Parent Relationships
    # =========================

    tenant: Mapped["Tenant"] = relationship(
        "Tenant"
    )

    workspace: Mapped["Workspace"] = relationship(
        "Workspace"
    )

    channel: Mapped["Channel"] = relationship(
        "Channel"
    )

    project: Mapped["Project"] = relationship(
        "Project",
        back_populates="tasks"
    )

    team: Mapped["Team"] = relationship(
        "Team",
        back_populates="tasks"
    )