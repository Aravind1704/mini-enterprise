<<<<<<< HEAD
from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    DateTime,
    Boolean,
    ForeignKey
)

from sqlalchemy.sql import func

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.database import Base




class PasswordResetToken(Base):

    __tablename__ = "password_reset_tokens"

   

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    

    token: Mapped[str] = mapped_column(
        String(512),
        unique=True,
        nullable=False
    )

    used: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )




class Plan(Base):

    __tablename__ = "plans"

    
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    

    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    price_cents: Mapped[int] = mapped_column(
        Integer
    )  

    credits: Mapped[int] = mapped_column(
        Integer
    )

    stripe_price_id: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True
    )



=======
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from app.database import Base


>>>>>>> 4500000c8c54ec045a9125ffb74854e6cb5209d2
class Subscription(Base):

    __tablename__ = "subscriptions"

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

    plan_id: Mapped[int | None] = mapped_column(
        ForeignKey("plans.id"),
        nullable=True
    )

   

    status: Mapped[str] = mapped_column(
        String(50),
        default="pending"
    )

    
    started_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    

    stripe_session_id: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True
    )




class CreditTransaction(Base):

    __tablename__ = "credit_transactions"

    

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

   

    organization_id: Mapped[int | None] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=True
    )

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    

    amount: Mapped[int] = mapped_column(
        Integer
    )  

    reason: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True
    )

    

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )
=======
    organization_id = Column(
        Integer,
        ForeignKey("organizations.id")
    )

    plan = Column(String)

    status = Column(
        String,
        default="active"
    )

    payment_provider = Column(String)
>>>>>>> 4500000c8c54ec045a9125ffb74854e6cb5209d2
