from app.repositories import (
    subscription_repo
)

PLANS = {

    "basic": 100,

    "silver": 500,

    "gold": 2000
}


def create_subscription_service(
    db,
    data
):

    credits = PLANS.get(
        data.plan.lower(),
        100
    )

    subscription = (
        subscription_repo
        .create_subscription(
            db,
            data
        )
    )

    return {

        "message":
        "Subscription Created",

        "plan":
        data.plan,

        "credits":
        credits,

        "subscription_id":
        subscription.id
    }


def get_subscriptions_service(
    db
):

    subscriptions = (
        subscription_repo
        .get_all_subscriptions(db)
    )

    return subscriptions