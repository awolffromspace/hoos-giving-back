from datetime import timedelta
from decimal import *
from django import forms
from django.core.exceptions import ValidationError

class MoneyDonationForm(forms.Form):
    money_splits = forms.CharField(label='Donation Splits', widget=forms.HiddenInput())

class TimeDonationForm(forms.Form):
    time_splits = forms.CharField(label='Volunteer Splits', widget=forms.HiddenInput())