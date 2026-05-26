from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Text
)

from sqlalchemy.sql import func

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.database import Base


# =====================================================
# SLA RULE MODEL
# =====================================================

class SLARule(Base):

    __tablename__ = "sla_rules"

    # =====================================================
    # PRIMARY KEY
    # =====================================================

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    # =====================================================
    # MODULE CONFIGURATION
    # =====================================================

    module_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )  # task / approval

    priority: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )  # low / medium / high

    # =====================================================
    # SLA SETTINGS
    # =====================================================

    allowed_hours: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    escalation_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    escalation_after_hours: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    # =====================================================
    # USER RELATION
    # =====================================================

    created_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    # =====================================================
    # TIMESTAMPS
    # =====================================================

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        onupdate=func.now()
    )


# =====================================================
# SLA TRACKING MODEL
# =====================================================

class SLATracking(Base):

    __tablename__ = "sla_tracking"

    # =====================================================
    # PRIMARY KEY
    # =====================================================

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    # =====================================================
    # MODULE INFO
    # =====================================================

    module_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    record_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )  # task_id or approval_id

    

    sla_rule_id: Mapped[int | None] = mapped_column(
        ForeignKey("sla_rules.id"),
        nullable=True
    )

    

    start_time: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    due_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    completed_time: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    

    status: Mapped[str] = mapped_column(
        String(50),
        default="active"
    )  # active / breached / completed

    breach_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        onupdate=func.now()
    )