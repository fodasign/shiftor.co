# coding=utf-8
"""Supervisor views."""
import logging, random
logger = logging.getLogger(__name__)

# Django imports
from django.core import signing
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate as dj_authenticate, login as dj_login, logout as dj_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Project imports
import singly.http
from utility import annoying as a
from utility import emails

# Internal imports
from . import auth
from .models import User
from .forms import EmailForm, LoginForm, SignupForm

def next (request):
    """Method of dubious dependability that handles a redirection."""
    if request.GET.get("next", None):
        request.session["next-url"] = request.GET.get("next")

    default = "/"
    if request.user.is_authenticated():
        if request.user.email == "blank@twitterlogin.com" or not request.user.password:
            default = reverse("supervisor.views.add_email")
        if not request.user.bartend_profile or not request.user.bar_profile:
            default = reverse("supervisor.views.complete_profile")
    return HttpResponseRedirect(request.session.get("next-url", default))

def login (request, out=None):
    if request.GET.get("next", None):
        request.session["next-url"] = request.GET.get("next")

    if request.user.is_authenticated():
        return next(request)
    if out:
        return HttpResponseRedirect(singly.http.connect(out, redirect_uri=request.build_absolute_uri(reverse("sv-bounce"))))
    data = {}
    form = LoginForm()
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            dj_login(request, form.cleaned_data.get("user"))
            return next(request)
    data["form"] = form
    return render(request, "supervisor/login.html", data)

def signup (request):
    data = {}
    form = SignupForm()
    if request.POST:
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User(username=form.cleaned_data.get("email"), **form.cleaned_data)
            user.set_password(form.cleaned_data.get("password"))
            if request.session.get("is_bar", False):
                user.is_bar = True
            else:
                user.is_bartend = True
            user.save()
            user = dj_authenticate(username=user.username, password=form.cleaned_data.get("password"))
            dj_login(request, user)
            return next(request)
    data["form"] = form
    return render(request, "supervisor/signup.html", data)

def logout (request):
    auth.logout(request)
    return next(request)

def bounce (request):
    """Handles bouncing after a Singly login."""
    code = request.GET.get("code")
    if code is None:
        return next(request)
    data = singly.http.fetch_token(code)

    if data is None:
        return HttpResponse("No result from singly. Authentication failed?")

    # This could probably be put into a separate logic function
    user = auth.login(request, data)
    return next(request)

def add_email (request):
    if not request.user.is_authenticated():
        return next(request)

    form = EmailForm()
    if request.POST:
        form = EmailForm(request.POST)
        if form.is_valid():
            request.user.email = form.cleaned_data.get("email")
            request.user.set_password(form.cleaned_data.get("password"))
            request.user.save()
            return next(request)
    return render(request, "supervisor/add_email.html", {"form" : form})