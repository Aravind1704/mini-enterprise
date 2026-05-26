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

<<<<<<< HEAD
    timestamp: datetime
=======
    old_values: Optional[str] = None

    new_values: Optional[str] = None

    changes_summary: Optional[str] = None

    change_reason: Optional[str] = None

    ip_address: Optional[str] = None

    timestamp: datetime

>>>>>>> 4500000c8c54ec045a9125ffb74854e6cb5209d2

    class Config:

        from_attributes = True