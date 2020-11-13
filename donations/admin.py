from django.contrib import admin

from .models import Charity, Task, MoneyDonation, TimeDonation

admin.site.register(Charity)
admin.site.register(Task)
admin.site.register(MoneyDonation)
admin.site.register(TimeDonation)