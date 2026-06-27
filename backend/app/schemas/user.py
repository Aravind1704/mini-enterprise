"""
User Schemas - Phase 4
Pydantic models for user validation and responses
"""

from pydantic import BaseModel, EmailStr
from typing import Optional


# =========================================================
# USER REGISTRATION SCHEMA
# =========================================================

class UserCreate(BaseModel):
    """Schema for user registration"""
    
    name: str
    email: EmailStr
    password: str
    role: str = "employee"
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "password": "SecurePass123",
                "role": "employee"
            }
        }


# =========================================================
# LOGIN SCHEMA
# =========================================================

class LoginRequest(BaseModel):
    """Schema for login request"""
    
    email: EmailStr
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "password": "SecurePass123"
            }
        }


# =========================================================
# USER OUTPUT SCHEMA
# =========================================================

class UserOut(BaseModel):
    """Schema for user response (no password)"""
    
    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool
    organization_id: Optional[int] = None
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "John Doe",
                "email": "john.doe@example.com",
                "role": "employee",
                "is_active": True,
                "organization_id": None
            }
        }


# =========================================================
# TOKEN RESPONSE SCHEMA
# =========================================================

class TokenResponse(BaseModel):
    """Schema for authentication token response"""
    
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserOut
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
                "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
                "token_type": "bearer",
                "user": {
                    "id": 1,
                    "name": "John Doe",
                    "email": "john.doe@example.com",
                    "role": "employee",
                    "is_active": True
                }
            }
        }


# =========================================================
# PASSWORD RESET SCHEMAS
# =========================================================

class ForgotPasswordRequest(BaseModel):
    """Schema for forgot password request"""
    
    email: EmailStr
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com"
            }
        }


class ResetPasswordRequest(BaseModel):
    """Schema for password reset"""
    
    token: str
    new_password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
                "new_password": "NewSecurePass123"
            }
        }


# =========================================================
# MESSAGE RESPONSE SCHEMAS
# =========================================================

class MessageResponse(BaseModel):
    """Generic message response"""
    
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Operation successful"
            }
        }


class TokenVerificationResponse(BaseModel):
    """Schema for token verification response"""
    
    valid: bool
    user: Optional[UserOut] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "valid": True,
                "user": {
                    "id": 1,
                    "name": "John Doe",
                    "email": "john.doe@example.com",
                    "role": "employee",
                    "is_active": True
                }
            }
        }
