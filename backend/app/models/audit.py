from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String(100))  # created, updated, deleted, etc
    entity = Column(String(100))  # Task, User, Document, etc
    entity_id = Column(Integer)
    details = Column(String(500), nullable=True)
    timestamp = Column(DateTime, server_default=func.now())