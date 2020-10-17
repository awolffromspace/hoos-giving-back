from django.conf import settings
from django.db import models

class MoneyDonation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    date_donated = models.DateTimeField('date donated')
    money_total = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return "{0} donated ${1} at {2}".format(
            self.user.username,
            self.money_total,
            self.date
        )

class TimeDonation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    date_donated = models.DateTimeField('date donated')
    time_total = models.DurationField()

    def __str__(self):
        return "{0} donated ${1} at {2}".format(
            self.user.username,
            self.time_total,
            self.date
        )