from sqlalchemy.orm import Session

from sqlalchemy import select

from app.models.subscription import (
    Subscription
)


def create_subscription(
    db: Session,
    data
):

    subscription = Subscription(

        organization_id=
        data.organization_id,

        plan=data.plan,

        payment_provider=
        data.payment_provider
    )

    db.add(subscription)

    db.commit()

    db.refresh(subscription)

    return subscription


def get_all_subscriptions(
    db: Session
):

    stmt = select(Subscription)

    result = db.execute(stmt)

    return result.scalars().all()