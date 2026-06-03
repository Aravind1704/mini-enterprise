from pydantic import (
    BaseModel,
    EmailStr
)

from typing import Optional

from datetime import datetime


class TenantCreate(BaseModel):

    name: str

    contact_email: EmailStr

    phone: Optional[str] = None

    address: Optional[str] = None

    industry: Optional[str] = None


class TenantUpdate(BaseModel):

    name: Optional[str] = None

    contact_email: Optional[EmailStr] = None

    phone: Optional[str] = None

    address: Optional[str] = None

    industry: Optional[str] = None

    status: Optional[str] = None


class TenantOut(BaseModel):

    id: int

    name: str

    slug: str

    contact_email: str

    phone: Optional[str]

    address: Optional[str]

    industry: Optional[str]

    status: str

    created_at: datetime

    updated_at: datetime

    class Config:
        from_attributes = True