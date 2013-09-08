# coding=utf-8
"""Auth and user management patterns."""

from django.conf.urls import patterns, include, url

urlpatterns = patterns("supervisor.views",
    url(r"^next$", "next", name="sv-next"),
    url(r"^login/?$", "login", name="sv-login"),
    url(r"^login/(?P<out>\S+)/?$", "login", name="sv-login-out"),
    url(r"^type/(?P<to>\S+)$", "toggle", name="sv-toggle"),
    url(r"^signup$", "signup", name="sv-signup"),
    url(r"^complete$", "complete_profile"),
    url(r"^profile$", "profile", name="sv-profile"),
    url(r"^billing$", "add_billing"),
    url(r"^logout/?$", "logout", name="sv-logout"),
    url(r"^bounce/?$", "bounce", name="sv-bounce"),
    url(r"^email/?$", "add_email"),
)