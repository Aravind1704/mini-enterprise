from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from app.models.comment import Comment
from app.models.task import Task
 
 
def get_task_by_id(task_id: int, db: Session):
    """Get a task by ID"""
    stmt = select(Task).where(Task.id == task_id)
    result = db.execute(stmt)
    return result.scalar_one_or_none()
 
 
def create_comment(
    task_id: int,
    user_id: int,
    content: str,
    is_internal: bool,
    db: Session
):
    """Create a new comment on a task"""
    comment = Comment(
        task_id=task_id,
        user_id=user_id,
        content=content,
        is_internal=is_internal
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment
 
 
def list_all_comments(task_id: int, db: Session):
    """List all comments on a task (admin view)"""
    stmt = (
        select(Comment)
        .where(Comment.task_id == task_id)
        .options(selectinload(Comment.user))
        .order_by(Comment.created_at.desc())
    )
    result = db.execute(stmt)
    return result.scalars().all()
 
 
def list_comments_for_manager(task_id: int, db: Session):
    """List all comments on a task (manager view - see internal notes)"""
    stmt = (
        select(Comment)
        .where(Comment.task_id == task_id)
        .options(selectinload(Comment.user))
        .order_by(Comment.created_at.desc())
    )
    result = db.execute(stmt)
    return result.scalars().all()
 
 
def list_comments_for_employee(task_id: int, db: Session):
    """
    List comments on a task (employee view - no internal notes).
    Employees only see public comments.
    """
    stmt = (
        select(Comment)
        .where(
            (Comment.task_id == task_id)
            & (Comment.is_internal == False)
        )
        .options(selectinload(Comment.user))
        .order_by(Comment.created_at.desc())
    )
    result = db.execute(stmt)
    return result.scalars().all()
 
 
def get_comment_by_id(comment_id: int, db: Session):
    """Get a single comment by ID"""
    stmt = (
        select(Comment)
        .where(Comment.id == comment_id)
        .options(selectinload(Comment.user))
    )
    result = db.execute(stmt)
    return result.scalar_one_or_none()
 
 
def update_comment(db: Session, comment_id: int, content: str):
    """Update a comment's content"""
    comment = get_comment_by_id(comment_id, db)
    if comment:
        comment.content = content
        db.commit()
        db.refresh(comment)
    return comment
 
 
def delete_comment(db: Session, comment_id: int):
    """Delete a comment"""
    comment = get_comment_by_id(comment_id, db)
    if comment:
        db.delete(comment)
        db.commit()
    return comment
 
 
def count_comments_on_task(task_id: int, db: Session):
    """Count total comments on a task"""
    stmt = (
        select(Comment)
        .where(Comment.task_id == task_id)
    )
    result = db.execute(stmt)
    comments = result.scalars().all()
    return len(comments)