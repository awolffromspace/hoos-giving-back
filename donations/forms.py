from datetime import timedelta
from django import forms

class MoneyDonationForm(forms.Form):
    money_total = forms.DecimalField(label='Money Total (USD)', max_digits=8, decimal_places=2, min_value=0.01)

class TimeDonationForm(forms.Form):
    time_total = forms.DurationField(label='Time Total (s)')

    def clean_time_total(self):
    	data = self.cleaned_data['time_total']
    	if data <= datetime.timedelta(0):
    		raise ValidationError("Your volunteer time must be positive")
    	return data