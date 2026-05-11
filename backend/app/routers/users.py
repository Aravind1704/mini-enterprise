from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import get_db

from app.models.user import User

from app.schemas.user import (
    UserOut
)

from app.core.dependencies import (
    require_role,
    get_current_user
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# ----------------------------
# GET ALL USERS
# ----------------------------

@router.get(
    "/",
    response_model=list[UserOut]
)
def list_users(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_role("admin")
    )
):

    stmt = select(User)

    result = db.execute(stmt)

    users = result.scalars().all()

    return users


# ----------------------------
# GET SINGLE USER
# ----------------------------

@router.get(
    "/{id}",
    response_model=UserOut
)
def get_user(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    stmt = (
        select(User)
        .where(User.id == id)
    )

    result = db.execute(stmt)

    user = result.scalar_one_or_none()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user