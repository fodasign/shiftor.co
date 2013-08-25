# coding=utf-8
import logging, uuid
from datetime import date
logger = logging.getLogger(__name__)

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.urlresolvers import reverse
from utility import annoying as a

class BartendProfile (models.Model):
    gender = models.CharField(max_length=255, choices=(("male", "Male"), ("female", "Female")))
    birthday = models.DateField()
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    student = models.BooleanField(verbose_name="Are you a student?")
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    photo = models.CharField(max_length=255)

    wk_name_1 = models.CharField(max_length=255, verbose_name="Work Place Name #1", null=True, blank=True)
    wk_type_1 = models.CharField(max_length=255, choices=(("Bartender", "Bartender"), ("Waiter / Waitress", "Waiter / Waitress"), ("Bar Back", "Bar Back"), ("Other", "Other")), verbose_name="Work Place Type #1", null=True, blank=True)
    wk_name_2 = models.CharField(max_length=255, verbose_name="Work Place Name #2", null=True, blank=True)
    wk_type_2 = models.CharField(max_length=255, choices=(("Bartender", "Bartender"), ("Waiter / Waitress", "Waiter / Waitress"), ("Bar Back", "Bar Back"), ("Other", "Other")), verbose_name="Work Place Type #2", null=True, blank=True)
    wk_name_3 = models.CharField(max_length=255, verbose_name="Work Place Name #3", null=True, blank=True)
    wk_type_3 = models.CharField(max_length=255, choices=(("Bartender", "Bartender"), ("Waiter / Waitress", "Waiter / Waitress"), ("Bar Back", "Bar Back"), ("Other", "Other")), verbose_name="Work Place Type #3", null=True, blank=True)
    wk_name_4 = models.CharField(max_length=255, verbose_name="Work Place Name #4", null=True, blank=True)
    wk_type_4 = models.CharField(max_length=255, choices=(("Bartender", "Bartender"), ("Waiter / Waitress", "Waiter / Waitress"), ("Bar Back", "Bar Back"), ("Other", "Other")), verbose_name="Work Place Type #4", null=True, blank=True)
    wk_name_5 = models.CharField(max_length=255, verbose_name="Work Place Name #5", null=True, blank=True)
    wk_type_5 = models.CharField(max_length=255, choices=(("Bartender", "Bartender"), ("Waiter / Waitress", "Waiter / Waitress"), ("Bar Back", "Bar Back"), ("Other", "Other")), verbose_name="Work Place Type #5", null=True, blank=True)

    years_exp = models.CharField(max_length=255, verbose_name="Number of Years in your Primary Industry", choices=(("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5+", "5+")))

    work_sports = models.BooleanField(verbose_name="Sports Bar/Pub")
    work_wine = models.BooleanField(verbose_name="Wine Bar")
    work_club = models.BooleanField(verbose_name="Club")
    work_lounge = models.BooleanField(verbose_name="Lounge")
    work_high = models.BooleanField(verbose_name="High-End Bar/Restaurant")
    work_event = models.BooleanField(verbose_name="Catering Hall/Event Space")

    available_mon = models.BooleanField(verbose_name="Available Monday")
    available_tue = models.BooleanField(verbose_name="Available Tuesday")
    available_wed = models.BooleanField(verbose_name="Available Wednesday")
    available_thu = models.BooleanField(verbose_name="Available Thursday")
    available_fri = models.BooleanField(verbose_name="Available Friday")
    available_sat = models.BooleanField(verbose_name="Available Saturday")
    available_sun = models.BooleanField(verbose_name="Available Sunday")

    work_pref_1 = models.CharField(max_length=255, choices=(("Bartender", "Bartender"), ("Waiter / Waitress", "Waiter / Waitress"), ("Bar Back", "Bar Back"), ("Other", "Other")), null=True, blank=True)
    work_pref_2 = models.CharField(max_length=255, choices=(("Bartender", "Bartender"), ("Waiter / Waitress", "Waiter / Waitress"), ("Bar Back", "Bar Back"), ("Other", "Other")), null=True, blank=True)
    work_pref_3 = models.CharField(max_length=255, choices=(("Bartender", "Bartender"), ("Waiter / Waitress", "Waiter / Waitress"), ("Bar Back", "Bar Back"), ("Other", "Other")), null=True, blank=True)
    work_pref_4 = models.CharField(max_length=255, choices=(("Bartender", "Bartender"), ("Waiter / Waitress", "Waiter / Waitress"), ("Bar Back", "Bar Back"), ("Other", "Other")), null=True, blank=True)

    licensed = models.BooleanField(verbose_name="Are you a licensed bartender?")
    licensed_upload = models.TextField(null=True, blank=True)

    pitch = models.TextField(verbose_name="Elevator Speech")

class BarProfile (models.Model):
    venue_name = models.CharField(max_length=255)
    email = models.EmailField()
    website = models.CharField(max_length=255)
    logo = models.CharField(max_length=255)
    address_1 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    photo = models.CharField(max_length=255)
    venue_type = models.CharField(max_length=255, choices=(
        ("sports", "Sports Bar/Pub"),
        ("wine", "Wine Bar"),
        ("club", "Club"),
        ("lounge", "Lounge"),
        ("high", "High-End Bar/Restaurant"),
        ("event", "Catering Hall/Event Space")))
    facebook_link = models.CharField(max_length=255, null=True, blank=True)
    twitter_link = models.CharField(max_length=255, null=True, blank=True)
    instagram_link = models.CharField(max_length=255, null=True, blank=True)

class User (AbstractUser):
    """Extended user model."""

    timezone = models.CharField(max_length=255, default="America/New_York")

    #: Singly account id
    singly_id = models.CharField(max_length=36, verbose_name="singly id", blank=True, null=True, unique=True, db_index=True, help_text="Automatically added when someone signs in or registers.")

    #: Singly ``access_token`` that is used to make requests.
    singly_token = models.CharField(max_length=255, verbose_name="singly access token", blank=True, null=True, help_text="Automatically added during signp.")

    is_bar = models.BooleanField(default=False)
    is_bartend = models.BooleanField(default=False)
    bartend_profile = models.ForeignKey(BartendProfile, null=True, blank=True)
    bar_profile = models.ForeignKey(BarProfile, null=True, blank=True)

    def __unicode__ (self):
        return u"{0} {1}".format(self.first_name, self.last_name)

    class Meta:
        ordering = ["-date_joined"]