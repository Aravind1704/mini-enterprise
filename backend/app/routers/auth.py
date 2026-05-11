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
    UserCreate,
    UserOut,
    LoginRequest,
    Token
)

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

from app.core.dependencies import (
    get_current_user
)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


# ----------------------------
# REGISTER
# ----------------------------

@router.post(
    "/register",
    response_model=UserOut
)
def register(
    data: UserCreate,
    db: Session = Depends(get_db)
):

    stmt = (
        select(User)
        .where(User.email == data.email)
    )

    result = db.execute(stmt)

    existing_user = result.scalar_one_or_none()

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    user = User(
        name=data.name,
        email=data.email,
        hashed_password=hash_password(data.password),
        role=data.role
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    return user


# ----------------------------
# LOGIN
# ----------------------------

@router.post(
    "/login",
    response_model=Token
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):

    stmt = (
        select(User)
        .where(User.email == data.email)
    )

    result = db.execute(stmt)

    user = result.scalar_one_or_none()

    if (
        not user
        or not verify_password(
            data.password,
            user.hashed_password
        )
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token(
        {"sub": user.email}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# ----------------------------
# CURRENT USER
# ----------------------------

@router.get(
    "/me",
    response_model=UserOut
)
def get_me(
    current_user=Depends(get_current_user)
):

    return current_user