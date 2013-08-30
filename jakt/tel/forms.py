# coding=utf-8
"""Todo forms."""

# Django imports
from django import forms
from django.contrib.auth.models import Group

# Internal imports
from .models import OutgoingNumber, valid_phonenumber

class OutgoingNumberForm (forms.ModelForm):
    class Meta:
        model = OutgoingNumber
        fields = ('number', )

    def clean_number (self):
        data = self.cleaned_data["number"]
        return valid_phonenumber(data, bitch=False)