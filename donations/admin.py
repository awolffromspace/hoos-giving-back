from django.contrib import admin

from .models import MoneyDonation, TimeDonation, MoneySplit, TimeSplit

admin.site.register(MoneyDonation)
admin.site.register(TimeDonation)
admin.site.register(MoneySplit)
admin.site.register(TimeSplit)