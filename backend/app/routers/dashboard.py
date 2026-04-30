from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.task import Task
from app.models.approval import Approval
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary")
def get_summary(db: Session = Depends(get_db), _=Depends(get_current_user)):
    tasks = db.query(Task).all()
    pending = db.query(Approval).filter(Approval.status == "pending").count()
    return {
        "total_tasks": len(tasks),
        "todo": sum(1 for t in tasks if t.status == "todo"),
        "in_progress": sum(1 for t in tasks if t.status == "in_progress"),
        "review": sum(1 for t in tasks if t.status == "review"),
        "done": sum(1 for t in tasks if t.status == "done"),
        "pending_approvals": pending
    }

@router.get("/task-distribution")
def task_distribution(db: Session = Depends(get_db), _=Depends(get_current_user)):
    tasks = db.query(Task).all()
    return [
        {"status": "todo", "count": sum(1 for t in tasks if t.status == "todo")},
        {"status": "in_progress", "count": sum(1 for t in tasks if t.status == "in_progress")},
        {"status": "review", "count": sum(1 for t in tasks if t.status == "review")},
        {"status": "done", "count": sum(1 for t in tasks if t.status == "done")},
    ]