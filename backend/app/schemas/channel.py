from pydantic import BaseModel

from typing import Optional

from datetime import datetime


class ChannelCreate(BaseModel):

    tenant_id: int

    workspace_id: int

    name: str

    description: Optional[str] = None

    channel_type: str = "PUBLIC"

    created_by: int



class ChannelUpdate(BaseModel):

    name: Optional[str] = None

    description: Optional[str] = None

    channel_type: Optional[str] = None

    is_archived: Optional[bool] = None


class ChannelOut(BaseModel):

    id: int

    tenant_id: int

    workspace_id: int

    name: str

    description: Optional[str]

    channel_type: str

    created_by: int

    is_archived: bool

    created_at: datetime

    updated_at: datetime

    class Config:
        from_attributes = True