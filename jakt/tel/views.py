# coding=utf-8
"""Basics views"""

import logging, json
logger = logging.getLogger(__name__)

# Django imports
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Project imports
from supervisor.decorators import requires_login
from utility.annoying import get_or_none as gon, get_or_gone as gog, tree_get

# Internal imports
from . import sms
from .models import IncomingNumber, OutgoingNumber, SMSLog
from .forms import OutgoingNumberForm

@requires_login
def list_numbers (request):
    numbers = OutgoingNumber.objects.filter(owner=request.user, deleted=False)
    form = OutgoingNumberForm()
    return render(request, "tel/list_numbers.html", { "numbers" : numbers, "form" : form })

@requires_login
def add_number (request):
    form = OutgoingNumberForm()
    if request.POST:
        form = OutgoingNumberForm(request.POST)
        if form.is_valid():
            number = form.save(commit=False)
            number.name = "{0}'s number".format(request.user)
            number.owner = request.user
            number.save()
            return HttpResponseRedirect(reverse("tel.views.send_verification", kwargs={"pk" : number.pk}))
    return render(request, "tel/add_number.html", { "form" : form })

@requires_login
def send_verification (request, pk):
    number = gog(OutgoingNumber, owner=request.user, pk=pk)
    if number.verified:
        return HttpResponseRedirect(reverse("tel.views.list_numbers"))

    code = number.roll_verification_code()
    sms.send(number, "Please enter the following code: {0}".format(code))
    return HttpResponseRedirect(reverse("tel.views.verify_number", kwargs={"pk" : number.pk}))

@requires_login
def verify_number (request, pk):
    number = gog(OutgoingNumber, owner=request.user, pk=pk)

    if number.verified:
        return HttpResponseRedirect(reverse("tel.views.list_numbers"))

    error = None
    if request.POST:
        code = request.POST.get("code", None)
        if code and code.upper().strip() == number.verification_code:
            number.verified = True
            number.save()
            sms.send(number, "Thanks! You can stop messages at any time by sending STOP")
            return HttpResponseRedirect(reverse("tel.views.list_numbers"))
        else:
            error = "The verification code didn't match."
    return render(request, "tel/verify_number.html", { "number" : number, "error" : error })

@requires_login
def delete_number (request, pk):
    return HttpResponse("Cannot delete numbers just yet.")

@sms.twilio_request
def incoming (request):
    n_incoming = tree_get(request.POST, "To", lambda s: s.strip())
    n_outgoing = tree_get(request.POST, "From", lambda s: s.strip())
    body = tree_get(request.POST, "Body", lambda s: s.strip())

    incoming = gon(IncomingNumber, number=n_incoming)
    outgoing = gon(OutgoingNumber, number=n_outgoing)

    if not incoming or not outgoing:
        logger.error("Unable to locate either {0} (in) or {1} (out)".format(n_incoming, n_outgoing))
        return

    SMSLog(incoming=incoming, outgoing=outgoing,
        body=body, raw=json.dumps(request.POST),
        direction=SMSLog.INCOMING).save()

    user = outgoing.owner
    todolist = gon(user.todolist_set)

    # Check to see if the body is an available action
    if body == "HELP":
        pass
    elif body == "STOP":
        sms.send(outgoing, "SMS messages stopped.")
        outgoing.deleted = True
        outgoing.save()
    return HttpResponse("")