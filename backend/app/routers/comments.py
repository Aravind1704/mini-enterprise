from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.comment import (
    CommentCreate,
    CommentOut
)

from app.core.dependencies import (
    get_current_user
)

from app.services.comment_service import (
    create_comment_service,
    list_comments_service
)

router = APIRouter(
    prefix="/tasks",
    tags=["Comments"]
)


# =====================================================
# CREATE COMMENT
# =====================================================

@router.post(
    "/{task_id}/comments",
    response_model=CommentOut
)
def create_comment(
    task_id: int,
    data: CommentCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):

    return create_comment_service(
        task_id,
        data,
        db,
        user
    )


# =====================================================
# LIST COMMENTS
# =====================================================

@router.get(
    "/{task_id}/comments",
    response_model=list[CommentOut]
)
def list_comments(
    task_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):

    return list_comments_service(
        task_id,
        db,
        user
    )