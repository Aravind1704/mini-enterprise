from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey
)

from sqlalchemy.sql import func

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.database import Base


class Notification(Base):

    __tablename__ = "notifications"

   

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    

    message: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    action_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    related_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

   

    is_read: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )