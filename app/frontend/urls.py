# coding=utf-8
"""Frontend url patterns"""
from django.conf.urls import patterns, include, url

urlpatterns = patterns("frontend.views",
    url(r"^$",    "home",               name="home"),

    # Error pages
    url(r"^500$", "internal_error",     name="internal-error"),
    url(r"^404$", "missing_error",      name="missing-error"),
    url(r"^403$", "forbidden_error",    name="forbidden-error"),
)