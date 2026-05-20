from sqlalchemy import (
    Column,
    Integer,
    String
)

from app.database import Base


class Organization(Base):

    __tablename__ = "organizations"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        unique=True
    )

    plan = Column(
        String,
        default="basic"
    )

    ai_credits = Column(
        Integer,
        default=100
    )