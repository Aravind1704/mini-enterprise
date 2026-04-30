from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.comment import Comment
from pydantic import BaseModel
from app.core.dependencies import get_current_user
from typing import Optional

class CommentCreate(BaseModel):
    content: str
    is_internal: Optional[bool] = False

router = APIRouter(prefix="/tasks", tags=["Comments"])

@router.post("/{id}/comments")
def create_comment(id: int, data: CommentCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    comment = Comment(task_id=id, user_id=current_user.id, content=data.content, is_internal=data.is_internal)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return {"id": comment.id, "task_id": comment.task_id, "user_id": comment.user_id, "content": comment.content, "is_internal": comment.is_internal, "created_at": comment.created_at}

@router.get("/{id}/comments")
def list_comments(id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    comments = db.query(Comment).filter(Comment.task_id == id).all()
    return [{"id": c.id, "task_id": c.task_id, "user_id": c.user_id, "content": c.content, "is_internal": c.is_internal, "created_at": c.created_at} for c in comments]