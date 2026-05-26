<<<<<<< HEAD
from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey
)

=======
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
>>>>>>> 4500000c8c54ec045a9125ffb74854e6cb5209d2
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
<<<<<<< HEAD

   

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
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
=======
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(String(20), default="todo")
    priority = Column(String(20), default="medium")
    due_date = Column(DateTime, nullable=True)
    
    created_by_id = Column(Integer, ForeignKey("users.id"))
    assigned_to_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Use strings "User" instead of the class User to avoid circular imports
    creator = relationship("User", foreign_keys=[created_by_id])
    assignee = relationship("User", foreign_keys=[assigned_to_id])

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
>>>>>>> 4500000c8c54ec045a9125ffb74854e6cb5209d2
