# app/services/email_service.py
<<<<<<< HEAD
import logging
from smtplib import SMTP, SMTPException
from email.message import EmailMessage
from typing import Optional
from app.core.config import settings

logger = logging.getLogger(__name__)

def send_email(to_email: str, subject: str, html_body: str, text_body: Optional[str] = None) -> None:
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.smtp_from_email
    msg["To"] = to_email
    msg.set_content(text_body or "Please view this message in an HTML-capable client.")
    msg.add_alternative(html_body, subtype="html")

    try:
        with SMTP(settings.smtp_server, settings.smtp_port, timeout=10) as smtp:
            smtp.starttls()
            if settings.smtp_user and settings.smtp_password:
                smtp.login(settings.smtp_user, settings.smtp_password)
            smtp.send_message(msg)
            logger.info("Email sent to %s", to_email)
    except SMTPException as e:
        logger.exception("SMTP error sending email to %s: %s", to_email, e)
        raise
    except Exception as e:
        logger.exception("Unexpected error sending email to %s: %s", to_email, e)
        raise

def send_password_reset_email(email: str, reset_token: str, user_name: str) -> None:
    reset_link = f"{settings.frontend_url}/reset-password?token={reset_token}"
    html = (
        f"<p>Hi {user_name},</p>"
        f"<p>Click to reset your password (expires in 15 minutes): "
        f"<a href='{reset_link}'>Reset your password</a></p>"
    )
    text = f"Hi {user_name},\n\nReset your password: {reset_link}\n"
    send_email(email, "Reset your password", html, text)
=======

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
>>>>>>> 4500000c8c54ec045a9125ffb74854e6cb5209d2
