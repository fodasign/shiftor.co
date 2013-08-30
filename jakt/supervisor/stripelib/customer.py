# coding=utf-8
import logging, stripe
logger = logging.getLogger(__name__)

# Django imports
from django.conf import settings

# Internal imports
from .decorators import stripe_call

stripe.api_key = settings.STRIPE_SECRET

@stripe_call
def create (card=None, **kwargs):
    logger.debug("Creating customer with token {0}".format(card))
    return stripe.Customer.create(card=card, **kwargs)

@stripe_call
def find_by_id (stripe_id):
    logger.debug("Looking for customer attached to {0}".format(stripe_id))
    return stripe.Customer.retrieve(stripe_id)

def find (payment):
    return find_by_id(payment.stripe_id)

@stripe_call
def update_subscription (payment, **kwargs):
    customer_obj = find(payment)
    if not customer_obj.subscription:
        logger.error("Unable to update non-existent subscription")
        return None
    customer_obj.update_subscription(plan=payment.plan.name, **kwargs)

@stripe_call
def cancel_subscription (payment):
    try:
        customer_obj = find(payment)
        return customer_obj.cancel_subscription()
    except (stripe.InvalidRequestError) as e:
        logger.exception(e)