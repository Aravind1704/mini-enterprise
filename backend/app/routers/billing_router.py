from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import stripe
from datetime import datetime
from app.database import get_db
from app.models.subscription import Plan, Subscription, CreditTransaction
from app.models.organization import Organization
from app.core.config import settings
from app.routers.auth import get_current_user

stripe.api_key = settings.stripe_secret_key

router = APIRouter(prefix="/billing", tags=["Billing"])

@router.get("/plans")
def list_plans(db: Session = Depends(get_db)):
    return db.query(Plan).all()

@router.post("/subscriptions/checkout")
def create_checkout(plan_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    plan = db.query(Plan).get(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{"price": plan.stripe_price_id, "quantity": 1}],
        mode="payment",
        success_url=f"{settings.frontend_url}/subscription/success?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{settings.frontend_url}/subscription/cancel",
        metadata={"organization_id": str(current_user.organization_id), "plan_id": str(plan.id)}
    )
    sub = Subscription(organization_id=current_user.organization_id, plan_id=plan.id, stripe_session_id=session.id, status="pending")
    db.add(sub)
    db.commit()
    return {"checkout_url": session.url}

@router.post("/webhooks/stripe")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.stripe_webhook_secret)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid webhook")
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        org_id = int(session["metadata"]["organization_id"])
        plan_id = int(session["metadata"]["plan_id"])
        plan = db.query(Plan).get(plan_id)
        subscription = db.query(Subscription).filter(Subscription.stripe_session_id == session["id"]).first()
        if subscription:
            subscription.status = "active"
            subscription.started_at = datetime.utcnow()
            db.add(subscription)
        org = db.query(Organization).get(org_id)
        if org and plan:
            org.ai_credits = (org.ai_credits or 0) + (plan.credits or 0)
            tx = CreditTransaction(organization_id=org_id, amount=plan.credits or 0, reason=f"Purchase {plan.name}")
            db.add(org)
            db.add(tx)
        db.commit()
    return {"ok": True}

@router.get("/me/subscription")
def my_subscription(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    org = db.query(Organization).get(current_user.organization_id)
    sub = db.query(Subscription).filter(Subscription.organization_id == org.id, Subscription.status == "active").order_by(Subscription.started_at.desc()).first() if org else None
    plan = db.query(Plan).get(sub.plan_id) if sub else None
    return {"plan": plan.name if plan else "free", "credits": org.ai_credits or 0}
