from pydantic import BaseModel
from typing import Optional


# ==========================================
# CREATE SUBSCRIPTION
# ==========================================

class SubscriptionCreate(BaseModel):

    organization_id: int

    plan: str

    payment_provider: str


# ==========================================
# UPDATE SUBSCRIPTION
# ==========================================

class SubscriptionUpdate(BaseModel):

    plan: Optional[str] = None

    status: Optional[str] = None


# ==========================================
# RESPONSE SCHEMA
# ==========================================

class SubscriptionOut(BaseModel):

    id: int

    organization_id: int

    plan: str

    status: str

    payment_provider: str

    class Config:

        from_attributes = True