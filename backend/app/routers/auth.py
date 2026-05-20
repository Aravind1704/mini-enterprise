"""
Authentication Routes - Phase 4
JWT, OAuth, and password management
"""

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    Header
)

from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session

from authlib.integrations.starlette_client import OAuth

from jose import jwt, JWTError

from app.database import get_db

from app.models.user import User

from app.schemas.user import (
    UserCreate,
    UserOut,
    LoginRequest,
    TokenResponse
)

from app.core.config import settings

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token
)

from app.core.dependencies import (
    get_current_user,
    verify_refresh_token
)

from app.core.limiter import limiter

from app.services.auth_service import (
    generate_reset_token,
    verify_reset_token
)

from app.services.email_service import (
    send_password_reset_email
)

from app.core.cache import get_cache, set_cache


# =========================================================
# ROUTER
# =========================================================

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# =========================================================
# GOOGLE OAUTH CONFIG
# =========================================================

oauth = OAuth()

oauth.register(
    name="google",
    client_id=settings.google_client_id,
    client_secret=settings.google_client_secret,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile"
    }
)


# =========================================================
# REGISTER - Create New User
# =========================================================

@router.post("/register", response_model=UserOut)
def register(
    data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user
    
    **Required fields:**
    - name: Full name
    - email: Valid email address
    - password: Min 8 characters
    - role: admin, manager, or employee
    """

    # Check if user already exists
    existing_user = db.query(User).filter(
        User.email == data.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Validate password length
    if len(data.password) < 8:
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 8 characters"
        )

    # Validate role
    valid_roles = ["admin", "manager", "employee"]
    if data.role not in valid_roles:
        raise HTTPException(
            status_code=400,
            detail=f"Role must be one of: {', '.join(valid_roles)}"
        )

    # Create new user
    user = User(
        name=data.name,
        email=data.email,
        hashed_password=hash_password(data.password),
        role=data.role,
        is_active=True
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# =========================================================
# LOGIN - Traditional Email/Password Login
# =========================================================

@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")
def login(
    request: Request,
    data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login with email and password
    
    Returns:
    - access_token: JWT token (30 min expiry)
    - refresh_token: JWT token (7 days expiry)
    - user: User details
    """

    # Find user by email
    user = db.query(User).filter(
        User.email == data.email
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="User account is disabled"
        )

    # Generate tokens
    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": user
    }


# =========================================================
# REFRESH TOKEN - Get New Access Token (FIXED)
# =========================================================

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token
    
    **Header:**
    - Authorization: Bearer <refresh_token>
    
    Returns:
    - New access_token with updated expiry
    """

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header format. Use: Bearer <token>"
        )

    try:
        # Extract token from "Bearer <token>"
        refresh_token_str = authorization.split(" ")[1]

        # Verify refresh token
        payload = jwt.decode(
            refresh_token_str,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )

        email = payload.get("sub")

        if not email:
            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token"
            )

        # Get user from database
        user = db.query(User).filter(
            User.email == email
        ).first()

        if not user or not user.is_active:
            raise HTTPException(
                status_code=401,
                detail="User not found or inactive"
            )

        # Generate new access token
        access_token = create_access_token({"sub": email})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token_str,  # Return same refresh token
            "token_type": "bearer",
            "user": user
        }

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token"
        )
    except IndexError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header format"
        )


# =========================================================
# FORGOT PASSWORD - Request Password Reset
# =========================================================

@router.post("/forgot-password")
@limiter.limit("3/hour")
def forgot_password(
    request: Request,
    email: str,
    db: Session = Depends(get_db)
):
    """
    Request password reset token.
    Sends email with reset link (valid 15 minutes).
    """

    user = db.query(User).filter(
        User.email == email
    ).first()

    # Always return same message for security (don't reveal if email exists)
    if not user:
        return {
            "message": "If email exists, password reset link will be sent"
        }

    reset_token = generate_reset_token(email)

    try:
        send_password_reset_email(
            email=email,
            reset_token=reset_token,
            user_name=user.name
        )

    except Exception as e:
        print(f"Email error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to send reset email"
        )

    return {
        "message": "Password reset link sent to email"
    }


# =========================================================
# RESET PASSWORD - Change Password with Token
# =========================================================

@router.post("/reset-password")
def reset_password(
    token: str,
    new_password: str,
    db: Session = Depends(get_db)
):
    """
    Reset password using token from email
    
    **Body Parameters:**
    - token: Password reset token from email
    - new_password: New password (min 8 chars)
    
    Returns:
    - Success message
    """

    # Validate new password
    if len(new_password) < 8:
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 8 characters"
        )

    # Verify reset token
    email = verify_reset_token(token)

    if not email:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired reset token"
        )

    # Find user
    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Update password
    user.hashed_password = hash_password(new_password)
    db.commit()

    return {
        "message": "Password reset successfully"
    }


# =========================================================
# GOOGLE OAUTH LOGIN - Initiate Google Login
# =========================================================

@router.get("/google/login")
async def google_login(request: Request):
    """
    Initiate Google OAuth login flow.
    Redirects user to Google login page.
    """

    redirect_uri = settings.google_redirect_uri

    return await oauth.google.authorize_redirect(
        request,
        redirect_uri,
        prompt="select_account"
    )


# =========================================================
# GOOGLE OAUTH CALLBACK (FIXED: Better user creation logic)
# =========================================================

@router.get("/google/callback")
async def google_callback(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Handle Google OAuth callback.
    Creates user if doesn't exist (as employee, not admin).
    Returns tokens and redirect to frontend.
    """

    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail="Failed to authorize with Google"
        )

    user_info = token.get("userinfo")

    if not user_info:
        raise HTTPException(
            status_code=400,
            detail="Google user info not found"
        )

    email = user_info.get("email")
    name = user_info.get("name")

    if not email:
        raise HTTPException(
            status_code=400,
            detail="Email not provided by Google"
        )

    # CHECK EXISTING USER
    user = db.query(User).filter(
        User.email == email
    ).first()

    # CREATE USER (FIXED: Default role is 'employee', not 'admin')
    if not user:
        user = User(
            name=name or email.split("@")[0],
            email=email,
            hashed_password="GOOGLE_AUTH",  # Placeholder for OAuth users
            role="employee",  # FIXED: Default to employee, not admin
            is_active=True
        )

        db.add(user)
        db.commit()
        db.refresh(user)

    # Don't allow inactive users to login via OAuth
    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Your account has been disabled"
        )

    # CREATE TOKENS
    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email})

    # FRONTEND REDIRECT WITH TOKENS
    frontend_url = settings.frontend_url

    return RedirectResponse(
        url=(
            f"{frontend_url}/oauth-success"
            f"?access_token={access_token}"
            f"&refresh_token={refresh_token}"
            f"&user_id={user.id}"
            f"&user_name={user.name}"
            f"&user_email={user.email}"
            f"&user_role={user.role}"
        )
    )


# =========================================================
# GET CURRENT USER - Verify JWT and Get User
# =========================================================

@router.get("/me", response_model=UserOut)
def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user's profile
    
    Requires: Valid JWT access token in Authorization header
    
    Returns:
    - User details (id, name, email, role, is_active)
    """

    return current_user


# =========================================================
# LOGOUT - Invalidate Token (Optional)
# =========================================================

@router.post("/logout")
def logout(
    current_user: User = Depends(get_current_user)
):
    """
    Logout current user
    
    Note: JWT tokens are stateless, so logout is primarily
    for frontend cleanup. Token will still be valid until expiry.
    
    Frontend should clear: access_token, refresh_token from localStorage
    """

    return {
        "message": "Logged out successfully",
        "note": "Please clear tokens from localStorage"
    }


# =========================================================
# VERIFY TOKEN - Check if Token is Valid
# =========================================================

@router.get("/verify")
def verify_token_endpoint(
    current_user: User = Depends(get_current_user)
):
    """
    Verify that the provided JWT token is valid
    
    Returns:
    - valid: true if token is valid
    - user: User info if valid
    """

    return {
        "valid": True,
        "user": current_user
    }