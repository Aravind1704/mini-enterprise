from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Approval(Base):
    __tablename__ = "approvals"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    requested_by = Column(Integer, ForeignKey("users.id"))
    status = Column(String(20), default="pending")
    current_level = Column(String(20), default="manager")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

class ApprovalHistory(Base):
    __tablename__ = "approval_history"
    id = Column(Integer, primary_key=True, index=True)
    approval_id = Column(Integer, ForeignKey("approvals.id"))
    action_by = Column(Integer, ForeignKey("users.id"))
    action = Column(String(20))
    comment = Column(Text)
    created_at = Column(DateTime, server_default=func.now())