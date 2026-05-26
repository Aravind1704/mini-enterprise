<<<<<<< HEAD
from datetime import datetime

from sqlalchemy import (
=======
from sqlalchemy import (
    Column,
>>>>>>> 4500000c8c54ec045a9125ffb74854e6cb5209d2
    Integer,
    String,
    ForeignKey,
    DateTime
)

<<<<<<< HEAD
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)
=======
from datetime import datetime
>>>>>>> 4500000c8c54ec045a9125ffb74854e6cb5209d2

from app.database import Base


class Billing(Base):

    __tablename__ = "billings"

<<<<<<< HEAD
    

    id: Mapped[int] = mapped_column(
=======
    id = Column(
>>>>>>> 4500000c8c54ec045a9125ffb74854e6cb5209d2
        Integer,
        primary_key=True,
        index=True
    )

<<<<<<< HEAD
   

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
=======
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
>>>>>>> 4500000c8c54ec045a9125ffb74854e6cb5209d2
        DateTime,
        default=datetime.utcnow
    )