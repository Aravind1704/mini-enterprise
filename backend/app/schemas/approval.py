from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ApprovalCreate(BaseModel):
    title: str
    description: Optional[str] = None
    workspace_id: Optional[int] = None
    channel_id: Optional[int] = None


class ApprovalAction(BaseModel):
    action: str
    comment: Optional[str] = None


class ApprovalOut(BaseModel):
    id: int
    tenant_id: Optional[int] = None
    workspace_id: Optional[int] = None
    channel_id: Optional[int] = None
    title: str
    description: Optional[str]
    requested_by: int
    status: str
    current_level: str
    created_at: datetime

    class Config:
        from_attributes = True


class ApprovalHistoryOut(BaseModel):
    id: int
    approval_id: int
    action_by: int
    action: str
    comment: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
