from django import forms

class MoneyDonationForm(forms.Form):
    money_total = forms.DecimalField(label='Money Total', max_digits=8, decimal_places=2)

class TimeDonationForm(forms.Form):
    time_total = forms.DurationField(label='Time Total')