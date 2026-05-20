# app/services/email_service.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings


def send_password_reset_email(email: str, reset_token: str, user_name: str):
    """Send password reset email"""
    
    try:
        reset_link = f"{settings.frontend_url}/reset-password?token={reset_token}"
        
        message = MIMEMultipart("alternative")
        message["Subject"] = "Password Reset - Enterprise Task Manager"
        message["From"] = settings.smtp_from_email
        message["To"] = email

        html = f"""
        <html>
            <body style="font-family: Arial; line-height: 1.6;">
                <h2>Password Reset Request</h2>
                <p>Hi {user_name},</p>
                <p>Click the link below to reset your password (valid for 15 minutes):</p>
                <p>
                    <a href="{reset_link}" 
                       style="background: #4f46e5; color: white; padding: 10px 20px; 
                              text-decoration: none; border-radius: 5px;">
                        Reset Password
                    </a>
                </p>
                <p>Or copy this link:</p>
                <p>{reset_link}</p>
                <p>If you didn't request this, please ignore this email.</p>
                <hr>
                <p style="color: #888; font-size: 12px;">
                    Enterprise Task Manager - Phase 4
                </p>
            </body>
        </html>
        """

        message.attach(MIMEText(html, "html"))

        # Send email
        with smtplib.SMTP(settings.smtp_server, settings.smtp_port) as server:
            server.starttls()
            server.login(settings.smtp_user, settings.smtp_password)
            server.sendmail(settings.smtp_from_email, email, message.as_string())

        return True

    except Exception as e:
        print(f"Email error: {str(e)}")
        raise Exception(f"Failed to send email: {str(e)}")