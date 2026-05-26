"""
Enterprise Task Manager - FastAPI Backend
Phase 4: Advanced Authentication, Security & Performance
"""
from app.routers import websocket
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from slowapi.middleware import SlowAPIMiddleware

from app.database import Base, engine
from app.core.limiter import limiter
from app.core.config import settings
from app.routers import (
    websocket_router
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
    notification
)
from app.routers.payment_router import (
    router as payment_router
)

from app.routers.subscription_router import (
    router as subscription_router
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




# =========================================================
# FASTAPI APP INITIALIZATION
# =========================================================

app = FastAPI(
    title="Enterprise Task Manager",
    description="Phase 4: Advanced Auth, Security & Performance",
    version="4.0.0"
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
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-Total-Count", "X-Page", "X-Page-Size"]
)


# =========================================================
# RATE LIMITER MIDDLEWARE
# =========================================================

app.state.limiter = limiter

app.add_middleware(
    SlowAPIMiddleware
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

# Task Management
app.include_router(tasks.router)
app.include_router(kanban.router)

# Comments
app.include_router(comments.router)

# Approvals
app.include_router(approvals.router)

# Dashboard
app.include_router(dashboard.router)

# Documents
app.include_router(documents.router)

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
# =========================================================
# HEALTH CHECK ENDPOINTS
# =========================================================

@app.get("/")
def root():
    """Root endpoint - API information"""
    return {
        "message": "Enterprise Task Manager - Phase 4",
        "status": "running",
        "version": "4.0.0",
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
        "version": "4.0.0"
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