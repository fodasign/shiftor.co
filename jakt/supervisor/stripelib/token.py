# coding=utf-8
import logging, stripe
logger = logging.getLogger(__name__)

# Django imports
from django.conf import settings

# Internal imports
from .decorators import stripe_call

stripe.api_key = settings.STRIPE_SECRET

@stripe_call
def get_card (token):
    logger.debug("Fetching card for token {0}".format(token))
    return stripe.Token.retrieve(token)