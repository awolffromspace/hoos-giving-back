import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.views import generic
from itertools import chain
from operator import attrgetter

from .forms import MoneyDonationForm, TimeDonationForm
from .models import MoneyDonation, TimeDonation, MoneySplit, TimeSplit

class IndexView(generic.ListView):
    template_name = 'donations/index.html'
    context_object_name = 'donation_list'

    def get_queryset(self):
        all_donations = MoneyDonation.objects.none()
        if self.request.user.is_authenticated:
            money_donations = MoneyDonation.objects.filter(
                user=self.request.user
            )
            time_donations = TimeDonation.objects.filter(
                user=self.request.user
            )
            all_donations = sorted(
                chain(money_donations, time_donations),
                key=attrgetter('date_donated'),
                reverse = True
            )
        return all_donations

def donate(request):
    if request.method == 'POST':
        form = MoneyDonationForm(request.POST)
        if form.is_valid():
            donation = MoneyDonation(user=request.user, date_donated=timezone.now(), money_total=form.cleaned_data['money_total'])
            splits_string = form.cleaned_data['money_splits']
            splits = splits_string.split(",")
            sum = 0
            for i in range(len(splits)):
                sum += float(splits[i])
            if sum < 0.99 or sum > 1.0:
                return render(request, 'donations/donate.html', {'form': form})
            donation.save()
            margin = (1.0 - sum) / len(splits)
            for i in range(len(splits)):
                split = float(splits[i]) + margin
                MoneySplit(money_donation=donation, money_split=split).save()
            return HttpResponseRedirect('/donations/')
    else:
        form = MoneyDonationForm()
    return render(request, 'donations/donate.html', {'form': form})

def volunteer(request):
    if request.method == 'POST':
        form = TimeDonationForm(request.POST)
        if form.is_valid():
            time_donation = TimeDonation(user=request.user, date_donated=timezone.now(), time_total=form.cleaned_data['time_total'])
            time_donation.save()
            return HttpResponseRedirect('/donations/')
    else:
        form = TimeDonationForm()
    return render(request, 'donations/volunteer.html', {'form': form})