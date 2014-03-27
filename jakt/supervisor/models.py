# coding=utf-8
import logging, uuid
import re
from datetime import date
logger = logging.getLogger(__name__)

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.urlresolvers import reverse
from utility import annoying as a

from tel.models import OutgoingNumber
from tel import sms

class User (AbstractUser):
    """Extended user model."""

    timezone = models.CharField(max_length=255, default="America/New_York")

    #: Singly account id
    singly_id = models.CharField(max_length=36, verbose_name="singly id", blank=True, null=True, unique=True, db_index=True, help_text="Automatically added when someone signs in or registers.")

    #: Singly ``access_token`` that is used to make requests.
    singly_token = models.CharField(max_length=255, verbose_name="singly access token", blank=True, null=True, help_text="Automatically added during signp.")

    is_bar = models.BooleanField(default=False)
    is_bartend = models.BooleanField(default=False)

    def __unicode__ (self):
        return u"{0} {1}".format(self.first_name, self.last_name)

    class Meta:
        ordering = ["-date_joined"]

    def get_profile (self):
        Profile = BartendProfile
        if self.is_bar:
            Profile = BarProfile
        return a.get_or_none(Profile, owner=self)

    @property
    def picture (self):
        p = self.get_profile()
        if p:
            if self.is_bar:
                return p.logo
            return p.photo

    def get_phone_number (self):
        numbers = OutgoingNumber.objects.filter(owner=self, deleted=False)
        if numbers:
            return numbers[0]

    def message (self, profile):
        phone = self.get_phone_number()
        if phone:
            sms.send(phone, "Insert {0} is interested in you regarding a job opportunity! Check your email or Login to Shiftor for more information.".format(profile.venue_name))

class BartendProfile (models.Model):
    owner = models.ForeignKey(User)
    gender = models.CharField(max_length=255, choices=(("male", "Male"), ("female", "Female")))
    birthday = models.DateField()
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    student = models.BooleanField(verbose_name="Are you a student?")
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

    work_pref_1 = models.CharField(max_length=255, choices=(("Bartender", "Bartender"), ("Waiter / Waitress", "Waiter / Waitress"), ("Bar Back", "Bar Back"), ("Other", "Other")), verbose_name="work preference")
    work_pref_2 = models.CharField(max_length=255, choices=(("Bartender", "Bartender"), ("Waiter / Waitress", "Waiter / Waitress"), ("Bar Back", "Bar Back"), ("Other", "Other")), null=True, blank=True)
    work_pref_3 = models.CharField(max_length=255, choices=(("Bartender", "Bartender"), ("Waiter / Waitress", "Waiter / Waitress"), ("Bar Back", "Bar Back"), ("Other", "Other")), null=True, blank=True)
    work_pref_4 = models.CharField(max_length=255, choices=(("Bartender", "Bartender"), ("Waiter / Waitress", "Waiter / Waitress"), ("Bar Back", "Bar Back"), ("Other", "Other")), null=True, blank=True)

    licensed = models.BooleanField(verbose_name="Are you a licensed bartender?")
    licensed_upload = models.TextField(null=True, blank=True)

    pitch = models.TextField(verbose_name="Elevator Speech")

    @property
    def age (self):
        today = date.today()
        born = self.birthday
        try:
            birthday = born.replace(year=today.year)
        except ValueError: # raised when birth date is February 29 and the current year is not a leap year
            birthday = born.replace(year=today.year, day=born.day-1)
        if birthday > today:
            return today.year - born.year - 1
        else:
            return today.year - born.year

    @property
    def available_dates (self):
        dates = ["mon","tue","wed","thu","fri","sat","sun"]
        available = []
        for d in dates:
            if getattr(self, "available_{0}".format(d)):
                available.push(d)
        return ",".join(available)

    @property
    def available_work (self):
        types = ["sports","club","high","lounge","event","wine"]
        available = []
        for d in types:
            if getattr(self, "work_{0}".format(d)):
                available.push(d[0])
        return ",".join(available)

    @property
    def work_prefs (self):
        available = []
        for i in ["1", "2", "3", "4"]:
            if getattr(self, "work_pref_{0}".format(i)):
                available.push(getattr(self, "work_pref_{0}".format(i)))
        return ", ".join(available)

class BarProfile (models.Model):
    owner = models.ForeignKey(User)
    venue_name = models.CharField(max_length=255)
    website = models.CharField(max_length=255)
    logo = models.CharField(max_length=255)
    address_1 = models.CharField(max_length=255, verbose_name="street")
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
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

    # Stripe
    customer_id = models.CharField(max_length=30, null=True, blank=True)
    card_4 = models.CharField(max_length=4, null=True, blank=True)

    def has_active_card (self):
        return not not self.customer_id

    @property
    def valid_website (self):
        ''' Returns valid website '''
        if not re.match('(?:http|ftp|https)://', self.website):
           url = '%s%s' % ('http://', self.website)
           return url