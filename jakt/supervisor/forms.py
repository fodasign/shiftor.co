# coding=utf-8
"""Supervisor forms."""

import logging, random
logger = logging.getLogger(__name__)

# Django imports
from django import forms
from django.contrib.auth import authenticate as dj_authenticate, login as dj_login
from django.core.exceptions import ValidationError

from .models import User, BartendProfile, BarProfile
from utility.annoying import get_or_none as gon
from utility import fields

class LoginForm (forms.Form):
    username = forms.CharField(max_length=30, label="Email")
    password = forms.CharField(widget=forms.PasswordInput)

    def clean (self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        if username and password:
            user = dj_authenticate(username=username.strip(), password=password)
            if user and user.is_active:
                cleaned_data["user"] = user
            else:
                raise forms.ValidationError("Invalid username or password")
        return cleaned_data

class SignupForm (forms.Form):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)
    terms = forms.BooleanField()

    def clean (self):
        cleaned_data = super(SignupForm, self).clean()
        email = cleaned_data.get("email")
        terms = cleaned_data.get("terms")

        if email:
            cleaned_data["email"] = email.strip().lower()
            if gon(User, email=cleaned_data["email"]):
                raise forms.ValidationError("That email address already exists.")
        return cleaned_data

class EmailForm (forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class BartendProfileForm (forms.ModelForm):
    birthday = forms.DateField(input_formats=["%m/%d/%Y"])
    class Meta:
        model = BartendProfile
        exclude = ('owner',)
class BarProfileForm (forms.ModelForm):
    class Meta:
        model = BarProfile
        exclude = ('owner', 'stripe_id', 'card_4')

class ChangePasswordForm (forms.Form):
    old_password = fields.PasswordField(mixin=[
        ("placeholder", "Current password"),
        ("required", True),
    ])
    old_password.widget.attrs.update({
            'class': '',
    })
    password = fields.PasswordField(mixin=[
        "autofocus",
        ("placeholder", "New password"),
        ("required", True),
    ])
    password.widget.attrs.update({
            'class': '',
    })

    def __init__ (self, *args, **kwargs):
        self.instance = kwargs.pop("instance", None)
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_old_password (self):
        password = self.cleaned_data.get("old_password")
        if self.instance and password:
            if not self.instance.check_password(password):
                raise ValidationError("Your current password did not match.",
                    code="invalid")
        return password

class ForgotPasswordForm (forms.Form):
    email = fields.EmailField(mixin=[
        "autofocus",
        "required",
        ("placeholder", "Account email address")
    ])
    email.widget.attrs.update({
            'class': '',
    })

class ResetPasswordForm (forms.Form):
    new_password = fields.PasswordField(mixin=[
        "autofocus",
        ("required", True),
        ("placeholder", "New Password")
    ])
    new_password.widget.attrs.update({
            'class': '',
    })
    repeat_new_password = fields.PasswordField(mixin=[
        ("required", True),
        ("placeholder", "Confirm Password")
    ])
    repeat_new_password.widget.attrs.update({
            'class': '',
    })

    def clean_repeat_new_password(self):
        new_password = self.cleaned_data.get("new_password")
        repeat_new_password = self.cleaned_data.get("repeat_new_password")
        if new_password and repeat_new_password and new_password != repeat_new_password:
            raise forms.ValidationError("New passwords did not match")
        return repeat_new_password