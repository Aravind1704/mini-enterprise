# app/services/email_service.py
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
