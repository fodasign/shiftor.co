# coding=utf-8
import logging, stripe
logger = logging.getLogger(__name__)

# Django imports
from django.conf import settings

# Internal imports
from .decorators import stripe_call

stripe.api_key = settings.STRIPE_SECRET

@stripe_call
def create (customer, amount, **kwargs):
    logger.debug("Charging customer {0} {1}¢".format(customer, amount))
    return stripe.Charge.create(amount=amount, currency="usd", customer=customer, **kwargs)