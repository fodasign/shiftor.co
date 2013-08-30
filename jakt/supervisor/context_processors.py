import pytz
from django.conf import settings

def timezone (request):
    """Adds the current timezone to the session."""
    return { "timezone" : request.session.get("timezone", settings.TIME_ZONE) }

def add_stripe_pk (request):
    return {
        "STRIPE_PUBLIC_KEY" : settings.STRIPE_PUBLIC
    }