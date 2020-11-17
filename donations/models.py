from django.conf import settings
from django.db import models

class Charity(models.Model):
    name = models.CharField(max_length=200, default='')
    desc = models.CharField(max_length=1000, default='')

    def __str__(self):
        return "{0}".format(
            self.name
        )

class Task(models.Model):
    name = models.CharField(max_length=200, default='')
    desc = models.CharField(max_length=1000, default='')

    def __str__(self):
        return "{0}".format(
            self.name
        )

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
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE)

    def __str__(self):
        return "{0} donated ${1} to {2} at {3}".format(
            self.user.username,
            self.money_total,
            self.charity.name,
            self.date_donated.strftime("%I:%M %p on %b %d %y")
        )

class TimeDonation(Donation):
    time_total = models.DurationField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return "{0} volunteered {1} minutes to do {2} at {3}".format(
            self.user.username,
            self.time_total.total_seconds() // 60,
            self.task.name,
            self.date_donated.strftime("%I:%M %p on %b %d %y")
        )