from django.conf import settings
from django.db import models

class Donation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    date_donated = models.DateTimeField('date donated')

    class Meta:
        abstract = True

class MoneyDonation(Donation):
    money_total = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return "{0} donated ${1} at {2}".format(
            self.user.username,
            self.money_total,
            self.date_donated
        )

class TimeDonation(Donation):
    time_total = models.DurationField()

    def __str__(self):
        return "{0} volunteered {1} time at {2}".format(
            self.user.username,
            self.time_total,
            self.date_donated
        )

class MoneySplit(models.Model):
    money_donation = models.ForeignKey(MoneyDonation, on_delete=models.CASCADE)
    money_split = models.DecimalField(max_digits=8, decimal_places=6)

class TimeSplit(models.Model):
    time_donation = models.ForeignKey(TimeDonation, on_delete=models.CASCADE)
    time_split = models.DecimalField(max_digits=8, decimal_places=6)