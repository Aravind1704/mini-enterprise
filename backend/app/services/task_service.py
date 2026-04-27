from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate


def create_task(data: TaskCreate, created_by_id: int, db: Session):
    # Validate assigned user exists if provided
    if data.assigned_to_id:
        user = db.query(User).filter(User.id == data.assigned_to_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Assigned user not found")

    task = Task(
        title=data.title,
        description=data.description,
        priority=data.priority or "medium",
        due_date=data.due_date,
        assigned_to_id=data.assigned_to_id,
        created_by_id=created_by_id,
        status="todo"
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_all_tasks(role: str, user_id: int, db: Session):
    if role == "admin":
        return db.query(Task).all()
    elif role == "manager":
        return db.query(Task).filter(Task.created_by_id == user_id).all()
    else:  # employee
        return db.query(Task).filter(Task.assigned_to_id == user_id).all()


def get_task_by_id(task_id: int, db: Session):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


def update_task(task_id: int, data: TaskUpdate, current_user, db: Session):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Employee can only update status of their own assigned task
    if current_user.role == "employee":
        if task.assigned_to_id != current_user.id:
            raise HTTPException(status_code=403, detail="You can only update your own tasks")
        if data.title or data.description or data.priority or data.due_date:
            raise HTTPException(status_code=403, detail="Employees can only update task status")

    for key, val in data.dict(exclude_unset=True).items():
        setattr(task, key, val)

    db.commit()
    db.refresh(task)
    return task


def delete_task(task_id: int, db: Session):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}


def assign_task(task_id: int, assigned_to_id: int, db: Session):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    user = db.query(User).filter(User.id == assigned_to_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User to assign not found")

    task.assigned_to_id = assigned_to_id
    db.commit()
    db.refresh(task)
    return task