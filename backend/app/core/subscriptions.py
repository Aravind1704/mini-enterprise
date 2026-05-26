from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.config import settings
from app.database import get_db
from app.models.subscription import CreditTransaction
from app.models.organization import Organization
from app.models.user import User
from app.routers.auth import get_current_user  # adjust import path if needed

def get_organization(db: Session, org_id: int) -> Organization:
    org = db.query(Organization).get(org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org

def add_credits(db: Session, organization_id: int, amount: int, reason: str = "admin_topup", user_id: int = None):
    org = get_organization(db, organization_id)
    org.ai_credits = (org.ai_credits or 0) + amount
    tx = CreditTransaction(organization_id=organization_id, user_id=user_id, amount=amount, reason=reason)
    db.add(org)
    db.add(tx)
    db.commit()
    return org.ai_credits

def require_credits(cost: int):
    """
    Dependency factory to require credits for an endpoint.
    Usage:
        @router.post("/ai/run")
        def run_ai(..., ok: bool = Depends(require_credits(10))):
            ...
    """
    def dependency(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
        org = db.query(Organization).get(current_user.organization_id)
        if (org.ai_credits or 0) < cost:
            raise HTTPException(status_code=402, detail="Insufficient credits")
        org.ai_credits -= cost
        tx = CreditTransaction(organization_id=org.id, user_id=current_user.id, amount=-cost, reason="AI usage")
        db.add(org)
        db.add(tx)
        db.commit()
        return True
    return dependency
