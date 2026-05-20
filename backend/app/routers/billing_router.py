from fastapi import APIRouter

from app.services.payment_service import (
    create_checkout_session
)

router = APIRouter(

    prefix="/billing",

    tags=["Billing"]
)


@router.get("/checkout")

def checkout():

    url = create_checkout_session()

    return {

        "checkout_url": url
    }