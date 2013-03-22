# coding=utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$',      include('frontend.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
