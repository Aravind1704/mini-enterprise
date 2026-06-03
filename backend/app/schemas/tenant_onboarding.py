from pydantic import BaseModel

from typing import Optional

from datetime import datetime


class TenantOnboardingCreate(BaseModel):

    tenant_id: int

    admin_user_id: Optional[int] = None


class TenantOnboardingOut(BaseModel):

    id: int

    tenant_id: int

    admin_user_id: Optional[int]

    onboarding_status: str

    default_workspace_created: bool

    settings_created: bool

    completed_at: Optional[datetime]

    created_at: datetime

    class Config:
        from_attributes = True