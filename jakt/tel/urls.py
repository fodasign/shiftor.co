# coding=utf-8
"""Tel url patterns"""

from django.conf.urls import patterns, include, url

urlpatterns = patterns("tel.views",
    url(r"^numbers/?$", "list_numbers", name="tel-list-numbers"),
    url(r"^new/?$", "add_number", name="tel-add-number"),
    url(r"^verify/(?P<pk>\d+)/send/?$", "send_verification", name="tel-verify-number-send"),
    url(r"^verify/(?P<pk>\d+)/?$", "verify_number", name="tel-verify-number"),
    url(r"^delete/(?P<pk>\d+)/?$", "delete_number", name="tel-delete-number"),
    url(r"^incoming/?$", "incoming", name="tel-incoming"),
)