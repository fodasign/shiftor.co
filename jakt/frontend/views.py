# coding=utf-8
"""Frontend views"""

import logging, os
logger = logging.getLogger(__name__)

# Django imports
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.core.exceptions import PermissionDenied

from supervisor.models import BartendProfile, BarProfile
from utility.annoying import get_or_gone as gog

def home (request):
    return render(request, "frontend/home.html")

def about (request):
    return render(request, "frontend/about.html", {"current": "about"})

def hiw (request):
    return render(request, "frontend/hiw.html", {"current": "hiw"})

def bars (request):
    bars = BarProfile.objects.all()
    return render(request, "frontend/bars.html", {"current": "bars", "bars" : bars})

def contact (request):
    return render(request, "frontend/contact.html", {"current": "contact"})

def privacy (request):
    return render(request, "frontend/privacy.html")

def tos (request):
    return render(request, "frontend/tos.html")

def search (request):
    profiles = BartendProfile.objects.all()
    return render(request, "frontend/search.html", { "profiles" : profiles })

def profile (request):
    pk = request.GET.get("pk")
    if not pk:
        raise Http404
    profile = gog(BartendProfile, pk=pk)
    return render(request, "frontend/profile_modal.html", {"profile" : profile})

def login (request):
    return render(request, "frontend/login.html")

def bartendersignup (request):
    return render(request, "frontend/bartendersignup.html")

def completebartenderprofile (request):
    return render(request, "frontend/completebartenderprofile.html")

def barsignup (request):
    return render(request, "frontend/barsignup.html")

def completebarprofile (request):
    return render(request, "frontend/completebarprofile.html")


def internal_error (request):
    return render(request, "frontend/internal_error.html")

def missing_error (request):
    return render(request, "frontend/missing_error.html")

def forbidden_error (request):
    return render(request, "frontend/forbidden_error.html")