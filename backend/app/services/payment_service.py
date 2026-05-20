from app.core.stripe_config import stripe


# =====================================================
# STRIPE PLANS
# =====================================================

PLANS = {

    "basic": {

        "price_id":
            "price_1TYrbFJOVlwW8VTxzgU1ZWeW",

        "credits": 100
    },

    "silver": {

        "price_id":
            "price_1TYrbhJOVlwW8VTxbbdDcHI2",

        "credits": 500
    },

    "gold": {

        "price_id":
            "price_1TYrc6JOVlwW8VTx4j6vJI4F",

        "credits": 2000
    }
}


# =====================================================
# CREATE CHECKOUT SESSION
# =====================================================

def create_checkout_session(plan: str):

    # =============================================
    # VALIDATE PLAN
    # =============================================

    if plan not in PLANS:

        raise Exception("Invalid plan")

    plan_data = PLANS[plan]

    # =============================================
    # CREATE STRIPE SESSION
    # =============================================

    session = stripe.checkout.Session.create(

        payment_method_types=["card"],

        mode="subscription",

        line_items=[

            {
                "price":
                    plan_data["price_id"],

                "quantity": 1
            }
        ],

        metadata={

            "plan": plan,

            "credits":
                plan_data["credits"]
        },

        success_url=
        "http://localhost:3000/success",

        cancel_url=
        "http://localhost:3000/cancel",
    )

    return session.url