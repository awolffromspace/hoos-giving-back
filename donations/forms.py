from datetime import timedelta
from decimal import *
from django import forms
from django.core.exceptions import ValidationError

class MoneyDonationForm(forms.Form):
    money_splits = forms.CharField(label='Donation Splits', widget=forms.HiddenInput())

class TimeDonationForm(forms.Form):
    time_splits = forms.CharField(label='Volunteer Splits', widget=forms.HiddenInput())

class TaskForm(forms.Form):
    name = forms.CharField(label='Task Name', max_length=50)
    desc = forms.CharField(label='Task Description', max_length=500, widget=forms.Textarea)