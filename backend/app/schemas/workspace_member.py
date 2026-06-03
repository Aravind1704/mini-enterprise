from pydantic import BaseModel
from datetime import datetime


# =========================================
# CREATE MEMBER
# =========================================

class WorkspaceMemberCreate(BaseModel):

    user_id: int

    role: str = "MEMBER"


# =========================================
# UPDATE ROLE
# =========================================

class WorkspaceMemberUpdateRole(BaseModel):

    role: str


# =========================================
# MEMBER RESPONSE
# =========================================

class WorkspaceMemberOut(BaseModel):

    id: int

    workspace_id: int

    user_id: int

    role: str

    joined_at: datetime

    is_active: bool

    class Config:
        from_attributes = True