
from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey
)


from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.database import Base

from app.models.user import User

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
        default="todo"
    )

    priority: Mapped[str] = mapped_column(
        String(20),
        default="medium"
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

    

    creator: Mapped["User"] = relationship(
        "User",
        foreign_keys=[created_by_id]
    )

    assignee: Mapped["User"] = relationship(
        "User",
        foreign_keys=[assigned_to_id]
    )

    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        onupdate=func.now()
    )

