# coding=utf-8
"""Utility models."""
import logging
logger = logging.getLogger(__name__)

# Django imports
from django.conf import settings
from django.db import models

# Reconfigure the user model maybe
User = settings.AUTH_USER_MODEL

class DatedModel (models.Model):
    """Adds created and updated fields for models."""
    created = models.DateTimeField(auto_now_add=True, help_text="Date created.")
    updated = models.DateTimeField(auto_now=True, help_text="Date last modified.")

    class Meta:
        """Meta nerd stuff here."""
        #: This is abstract, don't persist to the database
        abstract = True

class OwnedDatedModel (DatedModel):
    """Adds owner field to DatedModel."""
    owner = models.ForeignKey(User)
    class Meta:
        abstract = True