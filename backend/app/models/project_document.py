from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
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


class ProjectDocument(Base):
    __tablename__ = "project_documents"

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

    uploaded_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    file_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    file_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    file_size: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    mime_type: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    document_type: Mapped[str] = mapped_column(
        String(50),
        default="OTHER",
        nullable=False
    )

    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    tenant = relationship(
        "Tenant"
    )

    project = relationship(
        "Project",
        back_populates="documents"
    )
