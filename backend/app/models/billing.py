from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    ForeignKey,
    DateTime
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.database import Base


class Billing(Base):

    __tablename__ = "billings"

    

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

   

    organization_id: Mapped[int | None] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=True
    )

    

    amount: Mapped[int] = mapped_column(
        Integer
    )

    currency: Mapped[str] = mapped_column(
        String(20),
        default="INR"
    )

    payment_status: Mapped[str] = mapped_column(
        String(50),
        default="pending"
    )

    transaction_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )