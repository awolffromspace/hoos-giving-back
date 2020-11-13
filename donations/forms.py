from datetime import timedelta
from decimal import *
from django import forms
from django.core.exceptions import ValidationError

class MoneyDonationForm(forms.Form):
    money_total = forms.DecimalField(label='Money Total (USD)', max_digits=8, decimal_places=2, min_value=Decimal('0.01'))
    money_splits = forms.CharField(label='Donation Splits (Enter decimal fractions separated by ,)', widget=forms.HiddenInput())

class TimeDonationForm(forms.Form):
    time_total = forms.DurationField(label='Time Total (s)')
    time_splits = forms.CharField(label='Volunteer Splits (Enter decimal fractions separated by ,)')
    tasks = forms.CharField(label='Tasks (Enter tasks separated by ,)', max_length=200)

    def clean_time_total(self):
        data = self.cleaned_data['time_total']
        if data <= timedelta(0):
            raise ValidationError("Ensure this value is positive.")
        return data