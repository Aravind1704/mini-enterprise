from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.models import user, task, comment, approval

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Enterprise Task Manager - Phase 2")

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

@app.get("/")
def root():
    return {"status": "ok"}