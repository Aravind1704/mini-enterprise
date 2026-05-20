from datetime import (
    datetime,
    timedelta
)

from jose import jwt

from app.core.config import settings


# =====================================================
# GENERATE RESET TOKEN
# =====================================================

def generate_reset_token(
    email: str
):

    expire = datetime.utcnow() + timedelta(
        minutes=15
    )

    payload = {
        "sub": email,
        "exp": expire
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm
    )


# =====================================================
# VERIFY RESET TOKEN
# =====================================================

def verify_reset_token(
    token: str
):

    try:

        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )

        return payload.get("sub")

    except Exception:

        return None