from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NotificationOut(BaseModel):
    id: int
    user_id: int
    message: str
    action_type: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True