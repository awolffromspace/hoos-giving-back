from django.contrib import admin

from .models import MoneyDonation, TimeDonation

admin.site.register(MoneyDonation)
admin.site.register(TimeDonation)