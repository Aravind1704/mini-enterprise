from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from app.models.task import Task
 
 
def list_all_tasks(db: Session):
    """List all tasks with eager loading of relationships"""
    stmt = (
        select(Task)
        .options(
            selectinload(Task.assignee),
            selectinload(Task.creator)
        )
    )
    result = db.execute(stmt)
    return result.scalars().all()
 
 
def list_tasks_for_employee(db: Session, user_id: int):
    """List tasks assigned to a specific employee"""
    stmt = (
        select(Task)
        .where(Task.assigned_to_id == user_id)
        .options(
            selectinload(Task.assignee),
            selectinload(Task.creator)
        )
    )
    result = db.execute(stmt)
    return result.scalars().all()
 
 
def list_tasks_for_manager(db: Session, user_id: int):
    """List tasks created by or assigned to a manager"""
    stmt = (
        select(Task)
        .where(
            (Task.created_by_id == user_id)
            | (Task.assigned_to_id == user_id)
        )
        .options(
            selectinload(Task.assignee),
            selectinload(Task.creator)
        )
    )
    result = db.execute(stmt)
    return result.scalars().all()
 
 
def get_task_by_id(task_id: int, db: Session):
    """Get a single task by ID with relationships"""
    stmt = (
        select(Task)
        .where(Task.id == task_id)
        .options(
            selectinload(Task.assignee),
            selectinload(Task.creator)
        )
    )
    result = db.execute(stmt)
    return result.scalar_one_or_none()
 
 
def create_task(db: Session, task_data: dict):
    """Create a new task"""
    task = Task(**task_data)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task
 
 
def update_task(db: Session, task_id: int, task_data: dict):
    """Update an existing task"""
    task = get_task_by_id(task_id, db)
    if task:
        for key, value in task_data.items():
            if hasattr(task, key):
                setattr(task, key, value)
        db.commit()
        db.refresh(task)
    return task
 
 
def delete_task(db: Session, task_id: int):
    """Delete a task"""
    task = get_task_by_id(task_id, db)
    if task:
        db.delete(task)
        db.commit()
    return task