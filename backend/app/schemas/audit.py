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

    timestamp: datetime

    class Config:

        from_attributes = True