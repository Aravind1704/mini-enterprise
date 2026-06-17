from fastapi import (
    Depends,
    HTTPException,
    status
)

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from jose import (
    jwt,
    JWTError
)

from sqlalchemy.orm import Session

from typing import Optional

from app.database import get_db

from app.models.user import User

from app.core.config import settings


bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db)
) -> User:

    try:

        token = credentials.credentials

        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )

        email = payload.get("sub")

        if email is None:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        user = db.query(User).filter(
            User.email == email
        ).first()

        if user is None:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        if not user.is_active:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user"
            )

        return user

    except JWTError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )


def get_current_user_optional(
    credentials: Optional[
        HTTPAuthorizationCredentials
    ] = Depends(
        HTTPBearer(auto_error=False)
    ),
    db: Session = Depends(get_db)
):

    if credentials is None:
        return None

    try:

        token = credentials.credentials

        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )

        email = payload.get("sub")

        if email is None:
            return None

        user = db.query(User).filter(
            User.email == email
        ).first()

        return user

    except Exception:

        return None


# FIXED: Consolidated require_role function with flexible role checking
def require_role(*allowed_roles):
    """
    Role-based access control decorator.
    Accepts multiple roles and validates against current user.
    
    Usage:
        @router.get("/admin-only", dependencies=[Depends(require_role("admin"))])
        @router.get("/management", dependencies=[Depends(require_role("admin", "manager"))])
    """

    def role_checker(
        current_user: User = Depends(
            get_current_user
        )
    ):

        if current_user.role not in allowed_roles:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"This resource requires one of these roles: {', '.join(allowed_roles)}"
            )

        return current_user

    return role_checker


def require_admin(
    current_user: User = Depends(
        get_current_user
    )
):
    """
    Admin-only access control.
    Convenience wrapper for require_role("admin")
    """

    if current_user.role != "admin":

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return current_user


def require_manager(
    current_user: User = Depends(
        get_current_user
    )
):
    """
    Manager or Admin access control.
    Convenience wrapper for require_role("admin", "manager")
    """

    if current_user.role not in [
        "admin",
        "manager"
    ]:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Manager or Admin access required"
        )

    return current_user


def check_permission(
    user: User,
    resource_owner_id: int
):
    """
    Check if user has permission to access a resource.
    Admins can access everything, owners can access their own resources.
    """

    if user.role == "admin":
        return True

    if user.id == resource_owner_id:
        return True

    return False


def verify_refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db)
):
    """
    Verify refresh token and return user.
    Used for token refresh endpoints.
    """

    try:

        token = credentials.credentials

        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )

        email = payload.get("sub")

        if email is None:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        user = db.query(User).filter(
            User.email == email
        ).first()

        if user is None:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        if not user.is_active:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )

        return user

    except JWTError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )


def require_super_admin(
    current_user = Depends(get_current_user)
):

    if current_user.role != "super_admin":

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Super Admin access required"
        )

    return current_user