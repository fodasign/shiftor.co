# coding=utf-8

# Django imports
from django.contrib import admin

# Internal imports
from .models import IncomingNumber, OutgoingNumber, SMSLog

class IncomingNumberAdmin (admin.ModelAdmin):
    list_display = ('name', 'number', 'priority',)
    list_filter = ['priority',]

class OutgoingNumberAdmin (admin.ModelAdmin):
    list_display = ('name', 'owner', 'number', 'verification_code', 'verified', 'deleted',)
    list_filter = ['verified',]

class SMSLogAdmin (admin.ModelAdmin):
    list_display = ('incoming', 'outgoing', 'direction', 'created', 'body',)
    list_filter = ['direction',]

admin.site.register(IncomingNumber, IncomingNumberAdmin)
admin.site.register(OutgoingNumber, OutgoingNumberAdmin)
admin.site.register(SMSLog, SMSLogAdmin)
