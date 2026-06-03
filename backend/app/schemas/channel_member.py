from pydantic import BaseModel

from typing import Optional

from datetime import datetime


class ChannelMemberCreate(
    BaseModel
):

    user_id: int


class ChannelMemberOut(BaseModel):

    id: int

    channel_id: int

    user_id: int

    joined_at: datetime

    is_muted: bool

    last_read_message_id: Optional[int]

    class Config:
        from_attributes = True