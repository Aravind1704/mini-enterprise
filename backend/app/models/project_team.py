from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Integer,
    ForeignKey,
    DateTime
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from sqlalchemy.sql import func
from app.database import Base
from app.models.tenant import Tenant

if TYPE_CHECKING:
    from app.models.project import Project
    from app.models.Team import Team


class ProjectTeam(Base):
    __tablename__ = "project_teams"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    tenant_id: Mapped[int | None] = mapped_column(
        ForeignKey("tenants.id"),
        nullable=False
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False
    )

    team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id"),
        nullable=False
    )

    assigned_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    tenant: Mapped["Tenant"] = relationship(
        "Tenant"
    )

    project: Mapped["Project"] = relationship(
        "Project",
        back_populates="teams"
    )

    team: Mapped["Team"] = relationship(
        "Team",
        back_populates="project_teams"
    )
