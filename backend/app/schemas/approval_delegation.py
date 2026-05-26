from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ApprovalDelegationCreate(BaseModel):
    delegatee_id: int
    start_date: datetime
    end_date: datetime
    reason: str = Field(..., min_length=1)

class ApprovalDelegationOut(BaseModel):
    id: int
    delegator_id: int
    delegatee_id: int
    start_date: datetime
    end_date: datetime
    reason: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
