import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from slowapi.middleware import SlowAPIMiddleware
from sqlalchemy import inspect


from app.routers.tenant_routes import router as tenant_router
from app.routers.tenant_onboarding_routes import router as tenant_onboarding_router
from app.routers.tenant_collaboration_settings_routes import router as tenant_collaboration_settings_router
from app.routers.tenant_collaboration_usage_routes import router as tenant_collaboration_usage_router
from app.routers.workspace_routes import router as workspace_router
from app.routers.workspace_member_routes import router as workspace_member_router
from app.routers.channel_routes import router as channel_router
from app.routers.team_routes import router as team_router
from app.routers.project_routes import router as project_router
from app.routers.project_document_routes import router as project_document_router
from app.routers.meeting_routes import router as meeting_router
from app.routers.meeting_note_routes import router as meeting_note_router


from app.database import Base, engine
from app.core.limiter import limiter
from app.core.config import settings
from app.routers import (
    websocket_router
)
from app.routers.sla_routes import (
    router as sla_router,
    tracking_router
)


# =========================================================
# IMPORT MODELS (for table creation)
# =========================================================

from app.models import (
    user,
    task,
    comment,
    approval,
    audit,
    document,
    collaboration,
    notification
)
from app.routers.payment_router import (
    router as payment_router
)

from app.routers.subscription_router import (
    router as subscription_router
)
from app.routers.tenantdashboard_routes import (
    router as tenant_dashboard_router
)
# =========================================================
# IMPORT ROUTERS
# =========================================================

from app.routers import (
    auth,
    users,
    tasks,
    kanban,
    comments,
    approvals,
    dashboard,
    documents,
    collaboration,
    audit,
    notifications,
    ai,
    websocket
)
from app.routers import analytics_router


from app.routers import (
    subscription_router,
    payment_router,

)
from app.models.organization import Organization
from app.models.subscription import Subscription

from app.routers import sla_routes
from app.routers import approval_escalations, approval_delegations, notification_preferences, audit
# =========================================================
# CREATE TABLES
# =========================================================

Base.metadata.create_all(bind=engine)


def _ensure_column_exists(connection, table_name: str, column_name: str, column_sql: str) -> None:
    inspector = inspect(connection)
    if table_name not in inspector.get_table_names():
        return

    existing_columns = {column["name"] for column in inspector.get_columns(table_name)}
    if column_name in existing_columns:
        return

    connection.exec_driver_sql(column_sql)


def ensure_compatibility_schema() -> None:
    """
    Backfill columns that older databases may not have.

    The app now relies on these relationships in queries, but existing local
    databases may have been created before the Phase 10C migrations ran.
    """

    compatibility_columns = [
        ("users", "tenant_id", "ALTER TABLE users ADD COLUMN tenant_id INTEGER NULL"),
        ("users", "organization_id", "ALTER TABLE users ADD COLUMN organization_id INTEGER NULL"),
        ("teams", "tenant_id", "ALTER TABLE teams ADD COLUMN tenant_id INTEGER NULL"),
        ("teams", "workspace_id", "ALTER TABLE teams ADD COLUMN workspace_id INTEGER NULL"),
        ("teams", "name", "ALTER TABLE teams ADD COLUMN name VARCHAR(255) NULL"),
        ("teams", "description", "ALTER TABLE teams ADD COLUMN description VARCHAR(500) NULL"),
        ("teams", "created_by", "ALTER TABLE teams ADD COLUMN created_by INTEGER NULL"),
        ("teams", "is_active", "ALTER TABLE teams ADD COLUMN is_active BOOLEAN NULL"),
        ("teams", "created_at", "ALTER TABLE teams ADD COLUMN created_at DATETIME NULL"),
        ("teams", "updated_at", "ALTER TABLE teams ADD COLUMN updated_at DATETIME NULL"),
        ("team_members", "tenant_id", "ALTER TABLE team_members ADD COLUMN tenant_id INTEGER NULL"),
        ("team_members", "team_id", "ALTER TABLE team_members ADD COLUMN team_id INTEGER NULL"),
        ("team_members", "user_id", "ALTER TABLE team_members ADD COLUMN user_id INTEGER NULL"),
        ("team_members", "role", "ALTER TABLE team_members ADD COLUMN role VARCHAR(100) NULL"),
        ("team_members", "is_active", "ALTER TABLE team_members ADD COLUMN is_active BOOLEAN NULL"),
        ("team_members", "joined_at", "ALTER TABLE team_members ADD COLUMN joined_at DATETIME NULL"),
        ("projects", "tenant_id", "ALTER TABLE projects ADD COLUMN tenant_id INTEGER NULL"),
        ("projects", "workspace_id", "ALTER TABLE projects ADD COLUMN workspace_id INTEGER NULL"),
        ("projects", "owner_id", "ALTER TABLE projects ADD COLUMN owner_id INTEGER NULL"),
        ("projects", "name", "ALTER TABLE projects ADD COLUMN name VARCHAR(255) NULL"),
        ("projects", "description", "ALTER TABLE projects ADD COLUMN description TEXT NULL"),
        ("projects", "status", "ALTER TABLE projects ADD COLUMN status VARCHAR(50) NULL"),
        ("projects", "priority", "ALTER TABLE projects ADD COLUMN priority VARCHAR(50) NULL"),
        ("projects", "start_date", "ALTER TABLE projects ADD COLUMN start_date DATE NULL"),
        ("projects", "end_date", "ALTER TABLE projects ADD COLUMN end_date DATE NULL"),
        ("projects", "created_at", "ALTER TABLE projects ADD COLUMN created_at DATETIME NULL"),
        ("projects", "updated_at", "ALTER TABLE projects ADD COLUMN updated_at DATETIME NULL"),
        ("project_teams", "tenant_id", "ALTER TABLE project_teams ADD COLUMN tenant_id INTEGER NULL"),
        ("project_teams", "project_id", "ALTER TABLE project_teams ADD COLUMN project_id INTEGER NULL"),
        ("project_teams", "team_id", "ALTER TABLE project_teams ADD COLUMN team_id INTEGER NULL"),
        ("project_teams", "assigned_at", "ALTER TABLE project_teams ADD COLUMN assigned_at DATETIME NULL"),
        ("project_documents", "tenant_id", "ALTER TABLE project_documents ADD COLUMN tenant_id INTEGER NULL"),
        ("project_documents", "project_id", "ALTER TABLE project_documents ADD COLUMN project_id INTEGER NULL"),
        ("project_documents", "uploaded_by", "ALTER TABLE project_documents ADD COLUMN uploaded_by INTEGER NULL"),
        ("project_documents", "file_name", "ALTER TABLE project_documents ADD COLUMN file_name VARCHAR(255) NULL"),
        ("project_documents", "file_path", "ALTER TABLE project_documents ADD COLUMN file_path VARCHAR(500) NULL"),
        ("project_documents", "file_size", "ALTER TABLE project_documents ADD COLUMN file_size INTEGER NULL"),
        ("project_documents", "mime_type", "ALTER TABLE project_documents ADD COLUMN mime_type VARCHAR(255) NULL"),
        ("project_documents", "document_type", "ALTER TABLE project_documents ADD COLUMN document_type VARCHAR(50) NULL"),
        ("project_documents", "uploaded_at", "ALTER TABLE project_documents ADD COLUMN uploaded_at DATETIME NULL"),
        ("meetings", "tenant_id", "ALTER TABLE meetings ADD COLUMN tenant_id INTEGER NULL"),
        ("meetings", "project_id", "ALTER TABLE meetings ADD COLUMN project_id INTEGER NULL"),
        ("meetings", "title", "ALTER TABLE meetings ADD COLUMN title VARCHAR(255) NULL"),
        ("meetings", "description", "ALTER TABLE meetings ADD COLUMN description TEXT NULL"),
        ("meetings", "start_time", "ALTER TABLE meetings ADD COLUMN start_time DATETIME NULL"),
        ("meetings", "end_time", "ALTER TABLE meetings ADD COLUMN end_time DATETIME NULL"),
        ("meetings", "created_by", "ALTER TABLE meetings ADD COLUMN created_by INTEGER NULL"),
        ("meetings", "status", "ALTER TABLE meetings ADD COLUMN status VARCHAR(50) NULL"),
        ("meetings", "created_at", "ALTER TABLE meetings ADD COLUMN created_at DATETIME NULL"),
        ("meetings", "updated_at", "ALTER TABLE meetings ADD COLUMN updated_at DATETIME NULL"),
        ("meeting_attendees", "tenant_id", "ALTER TABLE meeting_attendees ADD COLUMN tenant_id INTEGER NULL"),
        ("meeting_attendees", "meeting_id", "ALTER TABLE meeting_attendees ADD COLUMN meeting_id INTEGER NULL"),
        ("meeting_attendees", "user_id", "ALTER TABLE meeting_attendees ADD COLUMN user_id INTEGER NULL"),
        ("meeting_attendees", "attendance_status", "ALTER TABLE meeting_attendees ADD COLUMN attendance_status VARCHAR(50) NULL"),
        ("meeting_notes", "tenant_id", "ALTER TABLE meeting_notes ADD COLUMN tenant_id INTEGER NULL"),
        ("meeting_notes", "meeting_id", "ALTER TABLE meeting_notes ADD COLUMN meeting_id INTEGER NULL"),
        ("meeting_notes", "notes", "ALTER TABLE meeting_notes ADD COLUMN notes TEXT NULL"),
        ("meeting_notes", "created_by", "ALTER TABLE meeting_notes ADD COLUMN created_by INTEGER NULL"),
        ("meeting_notes", "created_at", "ALTER TABLE meeting_notes ADD COLUMN created_at DATETIME NULL"),
        ("meeting_notes", "updated_at", "ALTER TABLE meeting_notes ADD COLUMN updated_at DATETIME NULL"),
        ("ai_meeting_summaries", "tenant_id", "ALTER TABLE ai_meeting_summaries ADD COLUMN tenant_id INTEGER NULL"),
        ("ai_meeting_summaries", "meeting_id", "ALTER TABLE ai_meeting_summaries ADD COLUMN meeting_id INTEGER NULL"),
        ("ai_meeting_summaries", "summary", "ALTER TABLE ai_meeting_summaries ADD COLUMN summary TEXT NULL"),
        ("ai_meeting_summaries", "action_items", "ALTER TABLE ai_meeting_summaries ADD COLUMN action_items TEXT NULL"),
        ("ai_meeting_summaries", "risks", "ALTER TABLE ai_meeting_summaries ADD COLUMN risks TEXT NULL"),
        ("ai_meeting_summaries", "decisions", "ALTER TABLE ai_meeting_summaries ADD COLUMN decisions TEXT NULL"),
        ("ai_meeting_summaries", "generated_at", "ALTER TABLE ai_meeting_summaries ADD COLUMN generated_at DATETIME NULL"),
        ("approvals", "tenant_id", "ALTER TABLE approvals ADD COLUMN tenant_id INTEGER NULL"),
        ("approvals", "workspace_id", "ALTER TABLE approvals ADD COLUMN workspace_id INTEGER NULL"),
        ("approvals", "channel_id", "ALTER TABLE approvals ADD COLUMN channel_id INTEGER NULL"),
        ("tasks", "tenant_id", "ALTER TABLE tasks ADD COLUMN tenant_id INTEGER NULL"),
        ("tasks", "workspace_id", "ALTER TABLE tasks ADD COLUMN workspace_id INTEGER NULL"),
        ("tasks", "channel_id", "ALTER TABLE tasks ADD COLUMN channel_id INTEGER NULL"),
        ("tasks", "project_id", "ALTER TABLE tasks ADD COLUMN project_id INTEGER NULL"),
        ("tasks", "team_id", "ALTER TABLE tasks ADD COLUMN team_id INTEGER NULL"),
        ("channels", "project_id", "ALTER TABLE channels ADD COLUMN project_id INTEGER NULL"),
    ]

    with engine.begin() as connection:
        for table_name, column_name, ddl_sql in compatibility_columns:
            try:
                _ensure_column_exists(connection, table_name, column_name, ddl_sql)
            except Exception:
                logger.exception("Failed to backfill %s.%s", table_name, column_name)


ensure_compatibility_schema()



# =========================================================
# FASTAPI APP INITIALIZATION
# =========================================================

app = FastAPI(
    title="Enterprise Task Manager",
    description="Phase 10C: Enterprise Teams, Projects, Meetings, and Collaboration",
    version="10.0.0"
)


# =========================================================
# SESSION MIDDLEWARE (MUST BE FIRST)
# =========================================================

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.secret_key,
    same_site="lax",
    https_only=False  # Set to True in production with HTTPS
)


# =========================================================
# RATE LIMITER MIDDLEWARE
# =========================================================

app.state.limiter = limiter

app.add_middleware(
    SlowAPIMiddleware
)


# =========================================================
# CORS MIDDLEWARE
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
        "http://localhost:3000",
        "http://localhost:8000"
    ],
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-Total-Count", "X-Page", "X-Page-Size"]
)


# =========================================================
# EXCEPTION HANDLERS
# =========================================================

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """
    Custom exception handler for validation errors.
    Returns detailed error information.
    """
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "errors": exc.errors()
        }
    )



# =========================================================
# INCLUDE ROUTERS
# =========================================================

app.include_router(websocket.router)

# Authentication
app.include_router(auth.router)

# User Management
app.include_router(users.router)



app.include_router(kanban.router)
# Task Management
app.include_router(tasks.router)


# Comments
app.include_router(comments.router)

# Approvals
app.include_router(approvals.router)

# Dashboard
app.include_router(dashboard.router)
app.include_router(tenant_dashboard_router)
    
# Documents
app.include_router(documents.router)
app.include_router(collaboration.router)

# Audit Logs
app.include_router(audit.router)

# Notifications
app.include_router(notifications.router)

# AI Features
app.include_router(ai.router)



app.include_router(
    analytics_router.router
)
app.include_router(subscription_router.router)

app.include_router(payment_router.router)


app.include_router(
    websocket_router.router
)


app.include_router(sla_routes.router)
app.include_router(sla_routes.tracking_router)
app.include_router(approval_escalations.router)
app.include_router(approval_delegations.router)
app.include_router(notification_preferences.router)
app.include_router(audit.router)
app.include_router(tenant_router)
app.include_router(tenant_onboarding_router)
app.include_router(tenant_collaboration_settings_router)
app.include_router(tenant_collaboration_usage_router)
app.include_router(workspace_router)
app.include_router(workspace_member_router)
app.include_router(channel_router)
app.include_router(team_router)
app.include_router(project_router)
app.include_router(project_document_router)
app.include_router(meeting_router)
app.include_router(meeting_note_router)
# =========================================================
# HEALTH CHECK ENDPOINTS
# =========================================================

@app.get("/")
def root():
    """Root endpoint - API information"""
    return {
        "message": "Enterprise Task Manager - Phase 10C",
        "status": "running",
        "version": "10.0.0",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }


@app.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "database": "connected",
        "cache": "connected",
        "version": "10.0.0"
    }


# =========================================================
# STARTUP & SHUTDOWN EVENTS
# =========================================================

@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    print("✅ Application started successfully")
    print(f"📍 Environment: {'Production' if settings.debug is False else 'Development'}")
    print(f"🔐 Security: JWT authentication enabled")
    print(f"⚡ Rate limiting: {'Enabled' if settings.rate_limit_enabled else 'Disabled'}")
    print(f"💾 Database: {settings.database_url}")
    print(f"🔗 Frontend URL: {settings.frontend_url}")
    print(f"📧 Email: {settings.smtp_from_email}")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""

    print("❌ Application shutting down...")



from app.core.sla_scheduler import start_scheduler

@app.on_event("startup")
def on_startup():
    start_scheduler()

    print("❌ Application shutting down...")

logger = logging.getLogger(__name__)
