from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ApprovalEscalationCreate(BaseModel):
    approval_id: int
    escalated_to: Optional[int] = None
    reason: str = Field(..., min_length=1)
    escalation_level: Optional[int] = 1

class ApprovalEscalationOut(BaseModel):
    id: int
    approval_id: int
    escalated_from: Optional[int]
    escalated_to: Optional[int]
    reason: Optional[str]
    escalation_level: int
    status: str
    escalated_at: datetime
    resolved_at: Optional[datetime]

    class Config:
        from_attributes = True
