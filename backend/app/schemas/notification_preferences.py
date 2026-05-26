from pydantic import BaseModel
from typing import Optional

class NotificationPreferencesUpdate(BaseModel):
    in_app_enabled: Optional[bool]
    email_enabled: Optional[bool]
    task_notifications: Optional[bool]
    approval_notifications: Optional[bool]
    escalation_notifications: Optional[bool]
    document_notifications: Optional[bool]

class NotificationPreferencesOut(BaseModel):
    id: int
    user_id: int
    in_app_enabled: bool
    email_enabled: bool
    task_notifications: bool
    approval_notifications: bool
    escalation_notifications: bool
    document_notifications: bool

    class Config:
        from_attributes = True
