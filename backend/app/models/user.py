from sqlalchemy import (
    Integer,
    String,
    Boolean,
    ForeignKey,
    Index
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)
from typing import TYPE_CHECKING


from app.database import Base
from sqlalchemy import ForeignKey


if TYPE_CHECKING:
    from app.models.organization import Organization
    
class User(Base):

    __tablename__ = "users"


   

    __table_args__ = (
        Index("idx_user_email", "email"),
    )

    

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

 

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    hashed_password: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    role: Mapped[str] = mapped_column(
        String(50),
        default="user"
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    

    organization_id: Mapped[int | None] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=True
    )

   

    organization: Mapped["Organization"] = relationship(
        "Organization",
        backref="users"
    )
