from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from itertools import chain
from operator import attrgetter

from .models import MoneyDonation, TimeDonation

class IndexView(generic.ListView):
    template_name = 'donations/index.html'
    context_object_name = 'donation_list'

    def get_queryset(self):
        money_donations = MoneyDonation.objects.filter(
            user=self.request.user
        )
        time_donations = TimeDonation.objects.filter(
            user=self.request.user
        )
        both_donations = sorted(
            chain(money_donations, time_donations)
        )
        return both_donations