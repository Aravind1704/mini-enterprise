from sqlalchemy.orm import Session
from app.models.task import Task
from app.models.approval import Approval
from datetime import datetime

def get_ai_summary(user_id: int, db: Session):
    tasks = db.query(Task).all()
    approvals = db.query(Approval).filter(Approval.status == "pending").all()
    
    high_priority = [t for t in tasks if t.priority == "high"]
    pending = [t for t in tasks if t.status == "todo"]
    overdue = [t for t in tasks if t.due_date and t.due_date < datetime.utcnow() and t.status != "done"]
    
    insights = {
        "total_tasks": len(tasks),
        "high_priority_tasks": len(high_priority),
        "pending_tasks": len(pending),
        "overdue_tasks": len(overdue),
        "pending_approvals": len(approvals),
        "summary": generate_summary(high_priority, pending, overdue, approvals)
    }
    
    return insights

def generate_summary(high_priority, pending, overdue, approvals):
    messages = []
    
    if high_priority:
        messages.append(f" {len(high_priority)} high priority tasks need attention")
    
    if pending:
        messages.append(f"{len(pending)} tasks pending")
    
    if overdue:
        messages.append(f"{len(overdue)} tasks are overdue")
    
    if approvals:
        messages.append(f"{len(approvals)} approvals waiting")
    
    if not messages:
        messages.append(" All systems nominal!")
    
    return " | ".join(messages)