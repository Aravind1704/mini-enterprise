from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ApprovalCreate(BaseModel):
    title: str
    description: Optional[str] = None

class ApprovalAction(BaseModel):
    action: str
    comment: Optional[str] = None

class ApprovalOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    requested_by: int
    status: str
    current_level: str
    created_at: datetime

    class Config:
        from_attributes = True