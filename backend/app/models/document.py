from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    DateTime,
    ForeignKey
)

from sqlalchemy.sql import func

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.database import Base


class Document(Base):

    __tablename__ = "documents"

   

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    

    file_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    file_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    version: Mapped[int] = mapped_column(
        Integer,
        default=1
    )

   

    uploaded_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    

    task_id: Mapped[int | None] = mapped_column(
        ForeignKey("tasks.id"),
        nullable=True
    )

    

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        onupdate=func.now()
    )