import datetime

from datetime import timedelta
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.views import generic
from itertools import chain
from operator import attrgetter

from .forms import MoneyDonationForm, TimeDonationForm
from .models import Charity, Task, MoneyDonation, TimeDonation

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

def processSplits(splits_str):
    if splits_str.endswith(','):
        splits_str = splits_str[0 : len(splits_str) - 1]
    splits_strlst = splits_str.split(',')
    splits = []
    sum = 0
    for i in range(len(splits_strlst)):
        try:
            split = float(splits_strlst[i])
            splits.append(split)
            sum += split
        except ValueError:
            return [-1]
    if sum < 0.01 or sum > 999999.99:
        return [-1]
    return splits

def donate(request):
    if request.method == 'POST':
        form = MoneyDonationForm(request.POST)
        if form.is_valid():
            splits = processSplits(form.cleaned_data['money_splits'])
            charities = Charity.objects.all()
            if splits[0] > -1:
                index = 0
                split = splits[index]
                for charity in charities:
                    if split > 0.00:
                        MoneyDonation(user=request.user, date_donated=timezone.now(), money_total=split, charity=charity).save()
            else:
                form = MoneyDonationForm()
                render(request, 'donations/donate.html', {'form': form})
            return HttpResponseRedirect('/donations/')
    else:
        form = MoneyDonationForm()
    return render(request, 'donations/donate.html', {'form': form})

def volunteer(request):
    if request.method == 'POST':
        form = TimeDonationForm(request.POST)
        if form.is_valid():
            splits = processSplits(form.cleaned_data['time_splits'])
            tasks = Task.objects.all()
            if splits[0] > -1:
                index = 0
                split = splits[index]
                for task in tasks:
                    if split > 0.00:
                        TimeDonation(user=request.user, date_donated=timezone.now(), time_total=timedelta(minutes=split), task=task).save()
            else:
                form = TimeDonationForm()
                render(request, 'donations/volunteer.html', {'form': form})
            return HttpResponseRedirect('/donations/')
    else:
        form = TimeDonationForm()
    return render(request, 'donations/volunteer.html', {'form': form})