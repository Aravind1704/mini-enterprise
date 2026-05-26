from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class SLARuleBase(BaseModel):
    module_name: str = Field(..., example="task")
    priority: str = Field(..., example="high")
    allowed_hours: int = Field(..., gt=0, example=24)
    escalation_enabled: bool = False
    escalation_after_hours: Optional[int] = None
    is_active: bool = True

    @validator("escalation_after_hours", always=True)
    def check_escalation(cls, v, values):
        if values.get("escalation_enabled") and (v is None or v <= 0):
            raise ValueError("escalation_after_hours must be > 0 when escalation_enabled is true")
        return v

class SLARuleCreate(SLARuleBase):
    pass

class SLARuleUpdate(BaseModel):
    module_name: Optional[str]
    priority: Optional[str]
    allowed_hours: Optional[int]
    escalation_enabled: Optional[bool]
    escalation_after_hours: Optional[int]
    is_active: Optional[bool]

class SLARuleOut(SLARuleBase):
    id: int
    created_by: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    class Config:
        from_attributes = True

class SLATrackingOut(BaseModel):
    id: int
    module_name: str
    record_id: int
    sla_rule_id: Optional[int]
    start_time: datetime
    due_time: datetime
    completed_time: Optional[datetime]
    status: str
    breach_reason: Optional[str]
    class Config:
        from_attributes = True
