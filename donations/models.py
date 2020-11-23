import pytz

from django.conf import settings
from django.db import models

class Charity(models.Model):
    name = models.CharField(max_length=50, default='')
    desc = models.CharField(max_length=500, default='')

    def __str__(self):
        return "{0}".format(
            self.name
        )

class Task(models.Model):
    name = models.CharField(max_length=50, default='')
    desc = models.CharField(max_length=500, default='')
    goal = models.IntegerField(default=0)
    fulfilled = models.BooleanField(default=False)

    def __str__(self):
        return "{0} has a goal of {1} minutes".format(
            self.name,
            self.goal
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
    money_total = models.DecimalField(max_digits=11, decimal_places=2)
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE)

    def __str__(self):
        level = Level.objects.filter(user=self.user).first().value
        return "Level {0} user {1} donated ${2} to {3} at {4}".format(
            level,
            self.user.username,
            self.money_total,
            self.charity.name,
            self.date_donated.astimezone(pytz.timezone('US/Eastern')).strftime("%I:%M %p on %b %d %y")
        )

class TimeDonation(Donation):
    time_total = models.IntegerField(default=0)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        level = Level.objects.filter(user=self.user).first().value
        return "Level {0} user {1} volunteered {2} minutes to do {3} at {4}".format(
            level,
            self.user.username,
            self.time_total,
            self.task.name,
            self.date_donated.astimezone(pytz.timezone('US/Eastern')).strftime("%I:%M %p on %b %d %y")
        )

class Level(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    value = models.IntegerField(default=1)

    def __str__(self):
        return "{0} is level {1}".format(
            self.user.username,
            self.value
        )