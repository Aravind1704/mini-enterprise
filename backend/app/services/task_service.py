from sqlalchemy.orm import Session
from fastapi import HTTPException
 
from app.models.task import Task
from app.models.user import User
from app.models.comment import Comment
from app.models.document import Document
from app.models.notification import Notification
 
from app.schemas.task import TaskCreate, TaskUpdate
from app.services.audit_service import log_action
 
 

def task_to_dict(task):
    """Convert task object to dictionary"""
    if not task:
        return None
    
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "priority": task.priority,
        "due_date": str(task.due_date) if task.due_date else None,
        "assigned_to_id": task.assigned_to_id,
        "created_by_id": task.created_by_id,
    }
 
 

 
def create_task(data: TaskCreate, created_by_id: int, db: Session):
    
    if data.assigned_to_id:
        user_exists = db.query(User).filter(
            User.id == data.assigned_to_id
        ).first()
        
        if not user_exists:
            raise HTTPException(
                status_code=404,
                detail="User to assign not found"
            )
    
 
    new_task = Task(
        title=data.title,
        description=data.description,
        priority=data.priority or "medium",
        due_date=data.due_date,
        status="todo",
        created_by_id=created_by_id,
        assigned_to_id=data.assigned_to_id
    )
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    
    log_action(
        db=db,
        user_id=created_by_id,
        action="CREATE",
        entity_type="Task",
        entity_id=new_task.id,
        details=f"Created task: {new_task.title}",
        new_values=task_to_dict(new_task)
    )
    
    return new_task
 
 

def get_all_tasks(role: str, user_id: int, db: Session):
    """
    Get tasks based on user role
    
    - Admin: sees all tasks
    - Manager: sees their own tasks + assigned tasks
    - Employee: sees only assigned tasks
    """
    
    if role == "admin":
        
        return db.query(Task).all()
    
    elif role == "manager":
        
        return db.query(Task).filter(
            (Task.created_by_id == user_id) |
            (Task.assigned_to_id == user_id)
        ).all()
    
    else:
        return db.query(Task).filter(
            Task.assigned_to_id == user_id
        ).all()
 
 

 
def get_task_by_id(task_id: int, db: Session):
   
    
    task = db.query(Task).filter(
        Task.id == task_id
    ).first()
    
    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )
    
    return task
 
 

 
def update_task(task_id: int, data: TaskUpdate, current_user, db: Session):

    

    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
  
    if current_user.role == "employee":
        if task.assigned_to_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="You can only update tasks assigned to you"
            )
    
  
    old_task_data = task_to_dict(task)
    
    
    changes_made = data.dict(exclude_unset=True)
    
    for field_name, field_value in changes_made.items():
        if field_value is not None:
            setattr(task, field_name, field_value)
    
    db.commit()
    db.refresh(task)
    
  
    new_task_data = task_to_dict(task)
    

    what_changed = []
    for field_name in new_task_data.keys():
        old_val = old_task_data.get(field_name)
        new_val = new_task_data.get(field_name)
        
        if old_val != new_val:
            what_changed.append(f"{field_name}: {old_val} → {new_val}")
    
    change_summary = " | ".join(what_changed) if what_changed else "No changes"
    
   
    log_action(
        db=db,
        user_id=current_user.id,
        action="UPDATE",
        entity_type="Task",
        entity_id=task.id,
        details=f"Updated task: {change_summary}",
        old_values=old_task_data,
        new_values=new_task_data,
        changes_summary=change_summary
    )
    
    return task
 
 

 
def update_task_status(task_id: int, new_status: str, current_user, reason: str = None, db: Session = None):
    """
    Change task status with optional reason
    
    Example: todo → in_progress → review → done
    """
    
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
   
    old_status = task.status
    old_task_data = task_to_dict(task)
    
    
    task.status = new_status
    db.commit()
    db.refresh(task)
    
    
    new_task_data = task_to_dict(task)
    
    
    summary = f"status: {old_status} → {new_status}"
    
    
    details = f"Status changed: {summary}"
    if reason:
        details += f" (Reason: {reason})"
    
    log_action(
        db=db,
        user_id=current_user.id,
        action="STATUS_CHANGE",
        entity_type="Task",
        entity_id=task.id,
        details=details,
        old_values=old_task_data,
        new_values=new_task_data,
        changes_summary=summary,
        change_reason=reason
    )
    
    return task
 
 

 
def assign_task(task_id: int, assigned_to_id: int, current_user, db: Session):
  
  
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Get the user to assign to
    target_user = db.query(User).filter(User.id == assigned_to_id).first()
    
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    

    if current_user.role == "manager":
       
        if target_user.role != "employee":
            raise HTTPException(
                status_code=403,
                detail="Managers can only assign tasks to employees"
            )
    
    elif current_user.role != "admin":
     
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to assign tasks"
        )
    
   
    old_assigned_to = task.assigned_to_id
    old_task_data = task_to_dict(task)
    
    
    task.assigned_to_id = assigned_to_id
    db.commit()
    db.refresh(task)
    
  
    new_task_data = task_to_dict(task)
    
    
    who_was_assigned = f"User #{old_assigned_to}" if old_assigned_to else "Unassigned"
    who_is_now = f"User #{assigned_to_id} ({target_user.name})"
    
    details = f"Task reassigned from {who_was_assigned} to {who_is_now}"
    
 
    log_action(
        db=db,
        user_id=current_user.id,
        action="ASSIGN",
        entity_type="Task",
        entity_id=task.id,
        details=details,
        old_values=old_task_data,
        new_values=new_task_data,
        changes_summary=f"assigned_to_id: {old_assigned_to} → {assigned_to_id}"
    )
    
    return task
 
 

 
def delete_task(task_id: int, current_user, db: Session):
   
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
   
    if current_user.role == "manager":
       
        if task.created_by_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="Managers can only delete their own tasks"
            )
    
    elif current_user.role == "employee":
  
        raise HTTPException(
            status_code=403,
            detail="Employees cannot delete tasks"
        )
    

    
    try:
        
        deleted_task_data = task_to_dict(task)
        
       
        db.query(Comment).filter(Comment.task_id == task_id).delete()
        

        db.query(Document).filter(Document.task_id == task_id).delete()
        
   
        db.query(Notification).filter(
            Notification.related_id == task_id
        ).delete()
        
   
        log_action(
            db=db,
            user_id=current_user.id,
            action="DELETE",
            entity_type="Task",
            entity_id=task_id,
            details=f"Deleted task: {task.title}",
            old_values=deleted_task_data
        )
        
    
        db.delete(task)
        db.commit()
        
        return {"message": "Task deleted successfully"}
    
    except Exception as error:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting task: {str(error)}"
        )