from pydantic import BaseModel

from datetime import datetime


class TenantCollaborationUsageOut(
    BaseModel
):

    id: int

    tenant_id: int

    workspace_count: int

    channel_count: int

    member_count: int

    storage_used_mb: int

    last_calculated_at: datetime

    class Config:
        from_attributes = True