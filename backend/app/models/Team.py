from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    Integer,
    Boolean,
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

if TYPE_CHECKING:
    from app.models.project_team import ProjectTeam
    from app.models.team_member import TeamMember
    from app.models.task import Task
    from app.models.tenant import Tenant
    from app.models.workspace import Workspace


class Team(Base):
    __tablename__ = "teams"

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

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
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

    tenant: Mapped["Tenant"] = relationship(
        "Tenant",
        back_populates="teams"
    )

    workspace: Mapped["Workspace"] = relationship(
        "Workspace",
        back_populates="teams"
    )

    members: Mapped[list["TeamMember"]] = relationship(
        "TeamMember",
        back_populates="team",
        cascade="all, delete-orphan"
    )

    project_teams: Mapped[list["ProjectTeam"]] = relationship(
        "ProjectTeam",
        back_populates="team",
        cascade="all, delete-orphan"
    )

    tasks: Mapped[list["Task"]] = relationship(
        "Task",
        back_populates="team"
    )
