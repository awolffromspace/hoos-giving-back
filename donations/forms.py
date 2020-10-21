from datetime import timedelta
from decimal import *
from django import forms
from django.core.exceptions import ValidationError

class MoneyDonationForm(forms.Form):
    money_total = forms.DecimalField(label='Money Total (USD)', max_digits=8, decimal_places=2, min_value=Decimal('0.01'))

class TimeDonationForm(forms.Form):
    time_total = forms.DurationField(label='Time Total (s)')

    def clean_time_total(self):
        data = self.cleaned_data['time_total']
        if data <= timedelta(0):
            raise ValidationError("Ensure this value is greater than or equal to 1.")
        return data