from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.comment import Comment
from app.schemas.comment import CommentCreate

def add_comment(task_id: int, data: CommentCreate, user_id: int, user_role: str, db: Session):
    # Only admin/manager can add internal notes
    if data.is_internal and user_role == "employee":
        raise HTTPException(status_code=403, detail="Employees cannot add internal notes")

    comment = Comment(
        task_id=task_id,
        user_id=user_id,
        content=data.content,
        is_internal=data.is_internal
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

def get_comments(task_id: int, user_role: str, db: Session):
    if user_role in ["admin", "manager"]:
        return db.query(Comment).filter(Comment.task_id == task_id).all()
    # Employees only see public comments
    return db.query(Comment).filter(
        Comment.task_id == task_id,
        Comment.is_internal == False
    ).all()