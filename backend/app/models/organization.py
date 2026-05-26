from sqlalchemy import (

    Column,
    Integer,
    String
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)


from app.database import Base


class Organization(Base):

    __tablename__ = "organizations"

    

    id: Mapped[int] = mapped_column(



        
        primary_key=True,
        index=True
    )


   
    name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

   

    plan: Mapped[str] = mapped_column(
    
        default="basic"
    )

    

    ai_credits: Mapped[int] = mapped_column(
        
        default=100
    )