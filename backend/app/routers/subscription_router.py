from fastapi import APIRouter

router = APIRouter(

    prefix="/subscriptions",

    tags=["Subscriptions"]
)

current_subscription = {

    "plan": "Silver",

    "credits": 500
}


@router.get("/")

def get_subscriptions():

    return current_subscription


@router.get("/current")

def get_current_subscription():

    return current_subscription