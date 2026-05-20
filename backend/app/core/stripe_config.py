import stripe
from decouple import config

stripe.api_key = config("STRIPE_SECRET_KEY")