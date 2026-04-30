from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.task import Task
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/tasks", tags=["Kanban"])

@router.get("/kanban")
def get_kanban(db: Session = Depends(get_db), _=Depends(get_current_user)):
    tasks = db.query(Task).all()
    return {
        "todo": [{"id": t.id, "title": t.title, "status": t.status, "priority": t.priority, "description": t.description, "due_date": t.due_date} for t in tasks if t.status == "todo"],
        "in_progress": [{"id": t.id, "title": t.title, "status": t.status, "priority": t.priority, "description": t.description, "due_date": t.due_date} for t in tasks if t.status == "in_progress"],
        "review": [{"id": t.id, "title": t.title, "status": t.status, "priority": t.priority, "description": t.description, "due_date": t.due_date} for t in tasks if t.status == "review"],
        "done": [{"id": t.id, "title": t.title, "status": t.status, "priority": t.priority, "description": t.description, "due_date": t.due_date} for t in tasks if t.status == "done"],
    }

@router.patch("/{id}/status")
def update_status(id: int, payload: dict, db: Session = Depends(get_db), _=Depends(get_current_user)):
    from fastapi import HTTPException
    task = db.query(Task).filter(Task.id == id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.status = payload.get("status", task.status)
    db.commit()
    db.refresh(task)
    return task