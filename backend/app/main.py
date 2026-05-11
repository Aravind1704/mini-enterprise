from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.models import user, task, comment, approval
from app.routers import auth, users, tasks, kanban, comments, approvals, dashboard, documents, audit, notifications, ai
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Enterprise Task Manager - Phase 3")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.routers import auth, users, tasks, kanban, comments, approvals, dashboard

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(kanban.router)
app.include_router(comments.router)
app.include_router(approvals.router)
app.include_router(dashboard.router)
app.include_router(documents.router)
app.include_router(audit.router)
app.include_router(notifications.router)
app.include_router(ai.router)

@app.get("/")
def root():
    return {"status": "ok"}
