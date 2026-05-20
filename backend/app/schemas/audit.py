from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AuditLogOut(
    BaseModel
):

    id: int

    user_id: int

    action: str

    entity: str

    entity_id: int

    details: str

    old_values: Optional[str] = None

    new_values: Optional[str] = None

    changes_summary: Optional[str] = None

    change_reason: Optional[str] = None

    ip_address: Optional[str] = None

    timestamp: datetime


    class Config:

        from_attributes = True