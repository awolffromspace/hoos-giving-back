import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.views import generic
from itertools import chain
from operator import attrgetter

from .forms import MoneyDonationForm
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
            chain(money_donations, time_donations),
            key=attrgetter('date_donated')
        )
        return both_donations

def donate_money(request):
    if request.method == 'POST':
        form = MoneyDonationForm(request.POST)
        if form.is_valid():
            money_donation = MoneyDonation(user=request.user, date_donated=timezone.now(), money_total=form.cleaned_data['money_total'])
            money_donation.save()
            return HttpResponseRedirect('/donations/')
    else:
        form = MoneyDonationForm()
    return render(request, 'donations/donate_money.html', {'form': form})