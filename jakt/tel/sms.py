# coding=utf-8
"""Handles sending SMS messages."""

# Python imports
from functools import wraps
from twilio.rest import TwilioRestClient
from twilio.util import RequestValidator

# Django imports
from django.conf import settings
from django.utils.decorators import available_attrs
from django.http import HttpResponse

# Project imports

# Internal imports
from .models import SMSLog, IncomingNumber

def simple_shim (d, f=None):
    if callable(f):
        return d(f)
    return d

def decorator_shim (d, f, *a, **k):
    """Quick shim for the if func: return logic."""
    b = d(*a, **k)
    return simple_shim(b, f)

def twilio_request (func):
    def decorator (view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view (request, *args, **kwargs):
            validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)
            url = settings.TWILIO_CALLBACK_URL
            post = request.POST
            signature = request.META.get("HTTP_X_TWILIO_SIGNATURE")
            if not validator.validate(url, post, signature):
                return HttpResponse("Invalid call. Are you twilio?")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return simple_shim(decorator, func)

def send (to, body):
    assert to.deleted = False, "Cannot send SMS messages to a deleted number"
    if len(body) > 160:
        # Cut body up into many different sections
        n = 152
        chunks = [ body[i:i+n] for i in range(0, len(body), n) ]
        total = len(chunks)
        for part, chunk in enumerate(chunks):
            chunk = chunk + " ({0}/{1})".format(part + 1, total)
            send(to, chunk)
    else:
        client = TwilioRestClient()
        fr = IncomingNumber.objects.order_by("priority").get()
        SMSLog(incoming=fr, outgoing=to, body=body).save()
        client.sms.messages.create(to=to.number, from_=fr.number, body=body)