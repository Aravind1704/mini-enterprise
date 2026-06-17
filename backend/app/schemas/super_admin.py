from pydantic import BaseModel
from typing import Optional


class TenantCreate(BaseModel):

    name: str
    slug: str
    contact_email: str
    phone: Optional[str] = None
    address: Optional[str] = None
    industry: Optional[str] = None


class TenantAdminCreate(BaseModel):

    tenant_id: int
    name: str
    email: str
    password: str

    
class TenantAdminAssign(BaseModel):

    tenant_id: int
    tenant_admin_id: int