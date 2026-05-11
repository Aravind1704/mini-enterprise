from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import get_db

from app.models.comment import Comment
from app.models.task import Task

from app.schemas.comment import (
    CommentCreate,
    CommentOut
)

from app.core.dependencies import (
    get_current_user
)

from app.services.notification_service import (
    notify_comment_added
)

router = APIRouter(
    prefix="/tasks",
    tags=["Comments"]
)



@router.post(
    "/{id}/comments",
    response_model=CommentOut
)
def create_comment(
    id: int,
    data: CommentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    
    stmt = (
        select(Task)
        .where(Task.id == id)
    )

    result = db.execute(stmt)

    task = result.scalar_one_or_none()

    if not task:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    

    comment = Comment(
        task_id=id,
        user_id=current_user.id,
        content=data.content,
        is_internal=data.is_internal
    )

    db.add(comment)

    db.commit()

    db.refresh(comment)

   

    if (
        task.assigned_to_id
        and task.assigned_to_id != current_user.id
    ):

        notify_comment_added(
            task_id=task.id,
            task_title=task.title,
            commenter_name=current_user.name,
            assigned_to_id=task.assigned_to_id,
            db=db
        )

    return comment




@router.get(
    "/{id}/comments",
    response_model=list[CommentOut]
)
def list_comments(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    stmt = (
        select(Comment)
        .where(Comment.task_id == id)
    )

    result = db.execute(stmt)

    comments = result.scalars().all()

    return comments