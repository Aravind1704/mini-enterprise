from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"
    due_date: Optional[datetime] = None
    tenant_id: Optional[int] = None
    workspace_id: Optional[int] = None
    channel_id: Optional[int] = None
    project_id: Optional[int] = None
    team_id: Optional[int] = None
    assigned_to_id: Optional[int] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    channel_id: Optional[int] = None
    project_id: Optional[int] = None
    team_id: Optional[int] = None

class TaskAssign(BaseModel):
    assigned_to_id: int

class TaskOut(BaseModel):
    id: int
    tenant_id: Optional[int] = None
    workspace_id: Optional[int] = None
    channel_id: Optional[int] = None
    project_id: Optional[int] = None
    team_id: Optional[int] = None
    title: str
    description: Optional[str]
    status: str
    priority: str
    due_date: Optional[datetime]
    created_by_id: Optional[int] = None
    assigned_to_id: Optional[int]
    updated_by: Optional[int] = None

    class Config:
        from_attributes = True
