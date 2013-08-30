# coding=utf-8
import logging, random, phonenumbers
from datetime import datetime
logger = logging.getLogger(__name__)

# Django imports
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError

# Project imports
from utility import annoying as a
from utility.models import DatedModel

User = settings.AUTH_USER_MODEL

class OwnedDatedModel (DatedModel):
    #: ``User`` who owns whatever this model is.
    owner = models.ForeignKey(User)

    class Meta:
        #: Don't actually create a table for this, it's abstract!
        abstract = True

def generate_verification_code ():
    """Generates a six character short code for verifying outgoing numbers."""
    possible = "ABCDEFGHJKMNPQRSTWXYZ123456789"
    return "".join(random.choice(possible) for n in range(6))

class IncomingNumber (DatedModel):
    """Incoming number we send messages from."""
    name = models.CharField(max_length=255, default=generate_verification_code)
    number = models.CharField(max_length=32)
    priority = models.IntegerField(default=10)

    def __unicode__ (self):
        return self.name

def valid_phonenumber (v, bitch=True):
    if "+" not in v:
        v = "+1" + v
    try:
        n = phonenumbers.parse(v, None)
    except Exception as e:
        raise ValidationError(u"{0} is impossible to parse {1}.".format(v, e))
    if not phonenumbers.is_possible_number(n):
        raise ValidationError(u"{0} is not a possible phone number.".format(v))
    if not phonenumbers.is_valid_number(n):
        raise ValidationError(u"{0} is not a valid phone number.".format(v))
    f = phonenumbers.format_number(n, phonenumbers.PhoneNumberFormat.E164)
    if bitch:
        if v != f:
            raise ValidationError(u"{0} is not formatted to E164")
    return f

class OutgoingNumber (OwnedDatedModel):
    """Outgoing number we receive messages from."""
    name = models.CharField(max_length=255)
    number = models.CharField(max_length=32, validators=[valid_phonenumber], unique=True)
    verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=8, default=generate_verification_code)
    deleted = models.BooleanField(default=False)

    def __unicode__ (self):
        return self.number

    def roll_verification_code (self):
        code = generate_verification_code()
        self.verification_code = code
        self.save()
        return code

class SMSLog (DatedModel):
    """Log of incoming / outgoing numbers."""
    INCOMING = 0
    OUTGOING = 1

    incoming = models.ForeignKey(IncomingNumber)
    outgoing = models.ForeignKey(OutgoingNumber)
    raw = models.TextField(null=True)
    body = models.TextField()
    direction = models.IntegerField(max_length=1, choices=((INCOMING, "Incoming"), (OUTGOING, "Outgoing")), default=OUTGOING)

    def __unicode__ (self):
        return "{sender} to {to}".format(sender=self.incoming, to=self.outgoing)

    class Meta:
        ordering = ['-created']