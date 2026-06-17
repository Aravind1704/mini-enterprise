from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MessageCreate(BaseModel):
    content: str
    message_type: str = "TEXT"


class MessageUpdate(BaseModel):
    content: str


class WorkspaceMessageOut(BaseModel):
    id: int
    tenant_id: int
    workspace_id: int
    sender_id: int
    content: str
    message_type: str
    edited_at: Optional[datetime]
    deleted_at: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class ChannelMessageOut(BaseModel):
    id: int
    tenant_id: int
    workspace_id: int
    channel_id: int
    sender_id: int
    content: str
    message_type: str
    edited_at: Optional[datetime]
    deleted_at: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class ScopedTaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    due_date: Optional[datetime] = None
    assigned_to_id: Optional[int] = None


class TaskAssign(BaseModel):
    assigned_to_id: int


class ScopedTaskOut(BaseModel):
    id: int
    tenant_id: Optional[int]
    workspace_id: Optional[int]
    channel_id: Optional[int]
    title: str
    description: Optional[str]
    status: str
    priority: str
    due_date: Optional[datetime]
    created_by_id: Optional[int]
    assigned_to_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


class TaskDocumentOut(BaseModel):
    id: int
    tenant_id: int
    task_id: int
    file_name: str
    file_size: int
    mime_type: Optional[str]
    uploaded_by: int
    document_type: str
    created_at: datetime

    class Config:
        from_attributes = True


class ApprovalDocumentOut(BaseModel):
    id: int
    tenant_id: int
    approval_id: int
    file_name: str
    file_size: int
    mime_type: Optional[str]
    uploaded_by: int
    document_type: str
    created_at: datetime

    class Config:
        from_attributes = True
