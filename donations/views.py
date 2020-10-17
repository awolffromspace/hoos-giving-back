from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from itertools import chain

from .models import MoneyDonation, TimeDonation

class IndexView(generic.ListView):
    template_name = 'donations/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['money_donations'] = MoneyDonation.objects.get(
        	user=self.request.user
        )
        context['time_donations'] = TimeDonation.objects.get(
        	user=self.request.user
        )
        return context