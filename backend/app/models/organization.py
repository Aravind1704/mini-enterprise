from sqlalchemy import (
<<<<<<< HEAD
=======
    Column,
>>>>>>> 4500000c8c54ec045a9125ffb74854e6cb5209d2
    Integer,
    String
)

<<<<<<< HEAD
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

=======
>>>>>>> 4500000c8c54ec045a9125ffb74854e6cb5209d2
from app.database import Base


class Organization(Base):

    __tablename__ = "organizations"
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
   
    name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

   

    plan: Mapped[str] = mapped_column(
        String(100),
        default="basic"
    )

    

    ai_credits: Mapped[int] = mapped_column(
=======
    name = Column(
        String,
        unique=True
    )

    plan = Column(
        String,
        default="basic"
    )

    ai_credits = Column(
>>>>>>> 4500000c8c54ec045a9125ffb74854e6cb5209d2
        Integer,
        default=100
    )