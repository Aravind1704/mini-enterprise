from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"
    due_date: Optional[datetime] = None
    assigned_to_id: Optional[int] = None

class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: Optional[str]
    priority: Optional[str]
    due_date: Optional[datetime]

class TaskAssign(BaseModel):
    assigned_to_id: int

class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    due_date: Optional[datetime]
    created_by_id: int
    assigned_to_id: Optional[int]

    class Config:
        from_attributes = True