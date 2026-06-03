from pydantic import BaseModel

from datetime import datetime


class TenantCollaborationSettingsCreate(
    BaseModel
):

    tenant_id: int

    max_workspaces: int = 10

    max_channels_per_workspace: int = 50

    max_workspace_members: int = 500

    max_storage_mb: int = 1024

    workspace_enabled: bool = True

    channel_enabled: bool = True


class TenantCollaborationSettingsUpdate(
    BaseModel
):

    max_workspaces: int | None = None

    max_channels_per_workspace: int | None = None

    max_workspace_members: int | None = None

    max_storage_mb: int | None = None

    workspace_enabled: bool | None = None

    channel_enabled: bool | None = None


class TenantCollaborationSettingsOut(
    BaseModel
):

    id: int

    tenant_id: int

    max_workspaces: int

    max_channels_per_workspace: int

    max_workspace_members: int

    max_storage_mb: int

    workspace_enabled: bool

    channel_enabled: bool

    created_at: datetime

    updated_at: datetime

    class Config:
        from_attributes = True