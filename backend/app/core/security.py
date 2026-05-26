from datetime import (
    datetime,
    timedelta
)

import bcrypt

from jose import jwt

from app.core.config import settings
from smtplib import SMTP
from email.message import EmailMessage

# =====================================================
# HASH PASSWORD
# =====================================================

def hash_password(password: str):

    password_bytes = password.encode("utf-8")


    salt = bcrypt.gensalt()

    hashed = bcrypt.hashpw(

        password_bytes,

        salt
    )

    return hashed.decode("utf-8")


# =====================================================
# VERIFY PASSWORD
# =====================================================

def verify_password(

    plain_password: str,

    hashed_password: str
):

    return bcrypt.checkpw(

        plain_password.encode("utf-8"),

        hashed_password.encode("utf-8")
    )


# =====================================================
# ACCESS TOKEN
# =====================================================

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(

        minutes=30
    )

    to_encode.update({

        "exp": expire
    })

    return jwt.encode(

        to_encode,

        settings.secret_key,

        algorithm=settings.algorithm
    )


# =====================================================
# REFRESH TOKEN
# =====================================================

def create_refresh_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(

        days=7
    )

    to_encode.update({

        "exp": expire
    })

    return jwt.encode(

        to_encode,

        settings.secret_key,

        algorithm=settings.algorithm
    )


# =====================================================
# VERIFY TOKEN
# =====================================================

def verify_token(token: str):

    try:

        payload = jwt.decode(

            token,

            settings.secret_key,

            algorithms=[settings.algorithm]
        )

        return payload

    except Exception:

        return None
    


  
def create_password_reset_token(user_email: str, expires_minutes: int = 60):
    payload = {
        "sub": user_email,
        "purpose": "password_reset",
        "exp": datetime.utcnow() + timedelta(minutes=expires_minutes)
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

def verify_password_reset_token(token: str):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        if payload.get("purpose") != "password_reset":
            return None
        return payload.get("sub")
    except Exception:
        return None



def send_email(to_email: str, subject: str, html_body: str, text_body: str = ""):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.smtp_from_email
    msg["To"] = to_email
    msg.set_content(text_body or html_body)
    msg.add_alternative(html_body, subtype="html")

    with SMTP(settings.smtp_server, settings.smtp_port) as smtp:
        smtp.starttls()
        smtp.login(settings.smtp_user, settings.smtp_password)
        smtp.send_message(msg)
