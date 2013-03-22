# coding=utf-8
"""Frontend views"""

import logging, os
logger = logging.getLogger(__name__)

# Django imports
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.exceptions import PermissionDenied

def home (request):
    return render(request, "frontend/home.html")

def internal_error (request):
    return render(request, "frontend/internal_error.html")

def missing_error (request):
    return render(request, "frontend/missing_error.html")

def forbidden_error (request):
    return render(request, "frontend/forbidden_error.html")