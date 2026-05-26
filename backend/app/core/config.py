"""
Application Configuration - Phase 4
Loaded from environment variables and .env file
"""

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables and .env file
    """
    
    # =========================================================
    # FRONTEND
    # =========================================================
    
    frontend_url: str = Field(
        default="http://localhost:3000",
        description="Frontend URL"
    )

    # =========================================================
    # DATABASE
    # =========================================================
    
    database_url: str = Field(
        default="sqlite:///./test.db",
        description="Database connection URL"
    )

    redis_url: str = Field(
        default="redis://localhost:6379",
        description="Redis connection URL for caching/sessions"
    )

    # =========================================================
    # SECURITY & JWT
    # =========================================================
    
    secret_key: str = Field(
        default="change-me-in-production-use-secrets-token-urlsafe",
        description="Secret key for JWT token signing (CHANGE IN PRODUCTION)"
    )

    algorithm: str = Field(
        default="HS256",
        description="JWT algorithm"
    )

    access_token_expire_minutes: int = Field(
        default=30,
        description="Access token expiration time in minutes"
    )

    refresh_token_expire_days: int = Field(
        default=7,
        description="Refresh token expiration time in days"
    )

    # =========================================================
    # GOOGLE OAUTH
    # =========================================================
    
    google_client_id: str = Field(
        default="",
        description="Google OAuth client ID"
    )

    google_client_secret: str = Field(
        default="",
        description="Google OAuth client secret"
    )

    google_redirect_uri: str = Field(
        default="http://127.0.0.1:8000/auth/google/callback",
        description="Google OAuth redirect URI"
    )

    # =========================================================
    # EMAIL/SMTP (FIXED: Added smtp_from_email)
    # =========================================================
    
    smtp_server: str = Field(
        default="smtp.gmail.com",
        description="SMTP server for sending emails"
    )

    smtp_port: int = Field(
        default=587,
        description="SMTP server port"
    )

    smtp_user: str = Field(
        default="",
        description="SMTP username/email address"
    )

    smtp_password: str = Field(
        default="",
        description="SMTP password or app-specific password"
    )

    smtp_from_email: str = Field(
        default="noreply@taskmanager.local",
        description="Email address to send from"
    )

    # =========================================================
    # APPLICATION
    # =========================================================
    
    app_name: str = Field(
        default="Enterprise Task Manager",
        description="Application name"
    )

    debug: bool = Field(
        default=True,
        description="Debug mode (set to False in production)"
    )

    # =========================================================
    # RATE LIMITING
    # =========================================================
    
    rate_limit_enabled: bool = Field(
        default=True,
        description="Enable API rate limiting"
    )

    # =========================================================
    # CONFIG CLASS
    # =========================================================
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()