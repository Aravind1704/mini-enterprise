from datetime import datetime

from sqlalchemy import (
    Integer,
    DateTime,
    Text,
    Boolean,
    ForeignKey
)

from sqlalchemy.sql import func

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.database import Base


class ApprovalDelegation(Base):

    __tablename__ = "approval_delegations"

   

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    
    delegator_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    delegatee_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

   

    start_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    end_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

   

    reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )