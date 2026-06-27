# app/models/project.py

from __future__ import annotations

from datetime import datetime, date
from typing import List

from sqlalchemy import (
    Integer,
    String,
    Text,
    Date,
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
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.channel import Channel
    from app.models.meeting import Meeting
    from app.models.project_document import ProjectDocument
    from app.models.project_team import ProjectTeam
    from app.models.task import Task
    from app.models.tenant import Tenant
    from app.models.user import User
    from app.models.workspace import Workspace

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    tenant_id: Mapped[int] = mapped_column(
        ForeignKey("tenants.id"),
        nullable=False
    )

    workspace_id: Mapped[int] = mapped_column(
        ForeignKey("workspaces.id"),
        nullable=False
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="PLANNED"
    )

    priority: Mapped[str] = mapped_column(
        String(50),
        default="MEDIUM"
    )

    start_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    end_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
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

    # =========================
    # Relationships
    # =========================

    tenant: Mapped["Tenant"] = relationship(
        "Tenant",
        back_populates="projects"
    )

    workspace: Mapped["Workspace"] = relationship(
        "Workspace",
        back_populates="projects"
    )

    owner: Mapped["User"] = relationship(
        "User",
        foreign_keys=[owner_id]
    )

    # MUST MATCH ProjectTeam.project
    teams: Mapped[List["ProjectTeam"]] = relationship(
        "ProjectTeam",
        back_populates="project",
        cascade="all, delete-orphan"
    )

    documents: Mapped[List["ProjectDocument"]] = relationship(
        "ProjectDocument",
        back_populates="project",
        cascade="all, delete-orphan"
    )

    meetings: Mapped[List["Meeting"]] = relationship(
        "Meeting",
        back_populates="project",
        cascade="all, delete-orphan"
    )

    channels: Mapped[List["Channel"]] = relationship(
        "Channel",
        back_populates="project"
    )

    tasks: Mapped[List["Task"]] = relationship(
        "Task",
        back_populates="project"
    )