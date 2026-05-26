from datetime import datetime

from sqlalchemy import (
    Integer,
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


class NotificationPreferences(Base):

    __tablename__ = "notification_preferences"

   

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

   

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    
    in_app_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    email_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    task_notifications: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    approval_notifications: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    escalation_notifications: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    document_notifications: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        onupdate=func.now()
    )