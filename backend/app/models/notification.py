from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String(500), nullable=False)
    action_type = Column(String(50))  # task_assigned, comment_added, approval_requested
    related_id = Column(Integer, nullable=True)  # task_id, approval_id, etc
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())