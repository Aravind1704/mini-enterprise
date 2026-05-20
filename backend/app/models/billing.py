from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)

from datetime import datetime

from app.database import Base


class Billing(Base):

    __tablename__ = "billings"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    organization_id = Column(
        Integer,
        ForeignKey("organizations.id")
    )

    amount = Column(Integer)

    currency = Column(
        String,
        default="INR"
    )

    payment_status = Column(
        String,
        default="pending"
    )

    transaction_id = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )