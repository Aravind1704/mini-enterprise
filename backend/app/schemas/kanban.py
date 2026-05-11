from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    due_date: Optional[datetime]

    class Config:
        from_attributes = True


class StatusUpdate(BaseModel):
    status: str