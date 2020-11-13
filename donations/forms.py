from datetime import timedelta
from decimal import *
from django import forms
from django.core.exceptions import ValidationError

class MoneyDonationForm(forms.Form):
    money_total = forms.DecimalField(label='Donation Total', max_digits=14, decimal_places=2, min_value=Decimal('0.01'), widget=forms.HiddenInput())
    money_splits = forms.CharField(label='Donation Splits', widget=forms.HiddenInput())

class TimeDonationForm(forms.Form):
    time_splits = forms.CharField(label='Volunteer Splits')