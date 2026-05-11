"""
Audit Log Schemas
File: app/schemas/audit.py

Pydantic models for validation and response formatting.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any


class AuditLogBase(BaseModel):
    """Base audit log schema"""
    
    user_id: Optional[int] = None
    action: str
    entity_type: str
    entity_id: int
    details: Optional[str] = None
    old_values: Optional[Dict[str, Any]] = None
    new_values: Optional[Dict[str, Any]] = None
    changes_summary: Optional[str] = None
    change_reason: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


class AuditLogCreate(BaseModel):
    """Create audit log"""
    
    action: str
    entity_type: str
    entity_id: int
    details: str
    old_values: Optional[Dict[str, Any]] = None
    new_values: Optional[Dict[str, Any]] = None
    changes_summary: Optional[str] = None
    change_reason: Optional[str] = None


class AuditLogOut(BaseModel):
    """Audit log response"""
    
    id: int
    user_id: Optional[int] = None
    action: str
    entity_type: str
    entity_id: int
    details: Optional[str] = None
    old_values: Optional[str] = None
    new_values: Optional[str] = None
    changes_summary: Optional[str] = None
    change_reason: Optional[str] = None
    ip_address: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class AuditLogList(BaseModel):
    """List of audit logs"""
    
    total: int
    skip: int
    limit: int
    logs: list[AuditLogOut]


class TaskAuditHistory(BaseModel):
    """Task audit history"""
    
    task_id: int
    total: int
    skip: int
    limit: int
    logs: list[AuditLogOut]


class FieldChangeHistory(BaseModel):
    """Field change history"""
    
    task_id: int
    field_name: str
    total_changes: int
    history: list[Dict[str, Any]]


class AuditStatistics(BaseModel):
    """Audit statistics"""
    
    days: int
    statistics: Dict[str, Any]