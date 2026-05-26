from datetime import datetime

from sqlalchemy import (
    Integer,
    Text,
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


class Comment(Base):

    __tablename__ = "comments"

   

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id"),
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    

    is_internal: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )