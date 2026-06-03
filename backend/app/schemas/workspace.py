from pydantic import BaseModel

from typing import Optional

from datetime import datetime


class WorkspaceCreate(BaseModel):

    tenant_id: int

    name: str

    description: Optional[str] = None

    avatar_url: Optional[str] = None

    visibility: str = "PUBLIC"

    created_by: int


class WorkspaceUpdate(BaseModel):

    name: Optional[str] = None

    description: Optional[str] = None

    avatar_url: Optional[str] = None

    visibility: Optional[str] = None

    is_archived: Optional[bool] = None


class WorkspaceOut(BaseModel):

    id: int

    tenant_id: int

    name: str

    slug: str

    description: Optional[str]

    avatar_url: Optional[str]

    visibility: str

    created_by: int

    is_archived: bool

    created_at: datetime

    updated_at: datetime

    class Config:
        from_attributes = True