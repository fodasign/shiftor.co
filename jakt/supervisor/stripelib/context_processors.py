from django.conf import settings

def add_public_key (request):
    return {
        "STRIPE_PUBLIC_KEY" : settings.STRIPE_PUBLIC
    }