from fastapi import (
    APIRouter,
    Request
)

import stripe

from app.services.payment_service import (
    create_checkout_session
)
from app.routers.subscription_router import (
    current_subscription
)

from app.core.config import settings



# =====================================================
# ROUTER
# =====================================================

router = APIRouter(

    prefix="/billing",

    tags=["Billing"]
)


# =====================================================
# FAKE DATABASE
# =====================================================

current_subscription = {

    "plan": "Silver",

    "credits": 500
}


# =====================================================
# CREATE CHECKOUT SESSION
# =====================================================

@router.get("/checkout/{plan}")

def checkout(plan: str):

    url = create_checkout_session(plan)

    return {

        "checkout_url": url
    }


# =====================================================
# STRIPE WEBHOOK
## =====================================================
# WEBHOOK
# =====================================================

@router.post("/webhook")

async def stripe_webhook(request: Request):

    payload = await request.body()

    sig_header = request.headers.get(

        "stripe-signature"
    )

    endpoint_secret = (
    settings.stripe_webhook_secret
)

    try:

        event = stripe.Webhook.construct_event(

            payload,

            sig_header,

            endpoint_secret
        )

    except Exception as e:

        print(e)

        return {

            "success": str(e)
        }

    # =================================================
    # PAYMENT SUCCESS
    # =================================================

    if event["type"] == \
        "checkout.session.completed":
        session = event["data"]["object"]

        plan = session["metadata"]["plan"]

        credits = int(
            session["metadata"]["credits"]
        )

        # UPDATE LIVE DATA

        current_subscription["plan"] = plan

        current_subscription["credits"] = credits

        print(f"✅ Updated Plan: {plan}")
        # =============================================
        # UPDATE CURRENT SUBSCRIPTION
        # =============================================

        current_subscription["plan"] = plan

        current_subscription["credits"] = \
            credits

        print(

            f"✅ Updated to {plan}"
        )

    return {

        "success": True
    }