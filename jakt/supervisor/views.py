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
from .models import User, BarProfile, BartendProfile
from .forms import EmailForm, LoginForm, SignupForm, BarProfileForm, BartendProfileForm
from .stripelib import customer

def next (request):
    """Method of dubious dependability that handles a redirection."""
    if request.GET.get("next", None):
        request.session["next-url"] = request.GET.get("next")

    default = "/"
    if request.user.is_authenticated():
        profile = request.user.get_profile()
        if request.user.email == "blank@twitterlogin.com" or not request.user.password:
            default = reverse("supervisor.views.add_email")
        elif not profile:
            default = reverse("supervisor.views.complete_profile")
        elif request.user.is_bartend and not request.user.get_phone_number():
            default = reverse("tel.views.add_number")
        elif settings.PAYWALL and request.user.is_bar and not profile.has_active_card():
            default = reverse("supervisor.views.add_billing")
        elif request.user.is_bar:
            default = reverse("frontend.views.search")
    return HttpResponseRedirect(request.session.pop("next-url", default))

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

def toggle (request, to):
    if to == "bar":
        request.session["is_bar"] = True
    else:
        request.session["is_bar"] = False
    return next(request)

def signup (request):
    if request.user.is_authenticated():
        return next(request)

    is_bar = request.session.get("is_bar", False)
    template = "supervisor/signup_bartend.html"
    if is_bar:
        template = "supervisor/signup_bar.html"

    data = { "is_bar" : is_bar }
    form = SignupForm()
    if request.POST:
        if request.POST.get("homepage"):
            form = SignupForm(initial={"email" : request.POST.get("email")})
        else:
            form = SignupForm(request.POST)
            if form.is_valid():
                user = User(username=form.cleaned_data.get("email"), **form.cleaned_data)
                user.set_password(form.cleaned_data.get("password"))
                if is_bar:
                    user.is_bar = True
                else:
                    user.is_bartend = True
                user.save()
                user = dj_authenticate(username=user.username, password=form.cleaned_data.get("password"))
                dj_login(request, user)
                return next(request)
    data["form"] = form
    return render(request, template, data)

def complete_profile (request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/")

    data = {}
    FormClass = BartendProfileForm
    template = "supervisor/complete_profile_bartender.html"
    if request.user.is_bar:
        FormClass = BarProfileForm
        template = "supervisor/complete_profile_bar.html"
    form = FormClass()
    logger.info(request.POST)
    if request.POST:
        form = FormClass(request.POST)
        if form.is_valid():
            model = form.save(commit=False)
            model.owner = request.user
            model.save()
            return next(request)
    data["form"] = form
    return render(request, template, data)

def profile (request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/")

    data = {}
    FormClass = BartendProfileForm
    template = "supervisor/complete_profile_bartender.html"
    profile = request.user.get_profile()
    if request.user.is_bar:
        FormClass = BarProfileForm
        template = "supervisor/complete_profile_bar.html"
    form = FormClass(instance=profile)
    logger.info(request.POST)
    if request.POST:
        form = FormClass(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile saved!")
    data["form"] = form
    return render(request, template, data)

def send_message (request):
    data = {}
    selected = request.POST.get("selected", "").split(",")
    users = filter(lambda u: not not u, map(lambda i: a.get_or_none(User, pk=i, is_bartend=True), selected))
    availables = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    data["days"] = days = []
    for av in availables:
        if request.POST.get("available_{0}".format(av[0:3]), False):
            days.append(av.title())
    for k in ["job_type", "job_duration", "details"]:
        data[k] = request.POST.get(k)

    profile = request.user.get_profile()
    for u in users:
        emails.send(request, "message", user=u,
                    bar=profile, **data)
        u.message(profile)
    return render(request, "supervisor/send_message.html", data)

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

    form = EmailForm(initial={"email" : request.user.email})
    if request.POST:
        form = EmailForm(request.POST)
        if form.is_valid():
            request.user.email = form.cleaned_data.get("email")
            request.user.set_password(form.cleaned_data.get("password"))
            request.user.save()
            return next(request)
    return render(request, "supervisor/add_email.html", {"form" : form})

def add_billing (request):
    if not request.user.is_authenticated():
        return next(request)
    profile = request.user.get_profile()
    if not profile:
        return next(request)
    err = ""
    if request.POST:
        stripeToken = request.POST.get("stripeToken")
        subscription_data = {
            "card" : stripeToken,
            "plan" : "SHIFT",
            "email" : request.user.email
        }
        stripe_user = customer.create(**subscription_data)
        if stripe_user:
            profile = request.user.get_profile()
            profile.customer_id = a.tree_get(stripe_user, "id")
            profile.card_4 = a.tree_get(stripe_user, "active_card", "last4")
            profile.save()
            return next(request)
        else:
            err = "Unable to verify your card. Please try again."
    return render(request, "supervisor/add_billing.html", { "err" : err })