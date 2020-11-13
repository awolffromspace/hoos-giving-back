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
        all_donations = MoneySplit.objects.none()
        if self.request.user.is_authenticated:
            money_donations = MoneySplit.objects.filter(
                money_donation__user=self.request.user
            ).order_by(
                '-money_donation__date_donated'
            )
            time_donations = TimeSplit.objects.filter(
                time_donation__user=self.request.user
            ).order_by(
                '-time_donation__date_donated'
            )
            all_donations = chain(money_donations, time_donations)
        return all_donations

def processSplits(splits_str):
    splits_strlst = splits_str.split(',')
    sum = 0
    nonzeroTotal = 0
    splits = []
    for i in range(len(splits_strlst) - 1):
        try:
            split = float(splits_strlst[i])
            splits.append(split)
            if split > 0.00:
                nonzeroTotal = nonzeroTotal + 1
        except ValueError:
            return [-1]
        else:
            sum += splits[i]
    if sum < 0.99 or sum > 1.0:
        return [-1]
    margin = (1.0 - sum) / nonzeroTotal
    for i in range(len(splits)):
        split = splits[i]
        if split > 0.00:
            splits[i] += margin
    return splits

def donate(request):
    if request.method == 'POST':
        form = MoneyDonationForm(request.POST)
        if form.is_valid():
            donation = MoneyDonation(user=request.user, date_donated=timezone.now(), money_total=form.cleaned_data['money_total'])
            splits = processSplits(form.cleaned_data['money_splits'])
            charities = ['The Trevor Project', 'The National Immigration Law Center', 'Human Rights Watch', 'The Global Fund for Women', 'Charity Water', 'Mental Health America']
            if splits[0] > -1 and len(splits) == len(charities):
                donation.save()
                for i in range(len(splits)):
                    split = round(splits[i], 4)
                    if split > 0.00:
                        MoneySplit(money_donation=donation, money_split=split, charity=charities[i]).save()
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
            volunteer = TimeDonation(user=request.user, date_donated=timezone.now(), time_total=form.cleaned_data['time_total'])
            splits = processSplits(form.cleaned_data['time_splits'])
            tasks = form.cleaned_data['tasks']
            tasks_lst = tasks.split(',')
            if splits[0] > -1 and len(splits) == len(tasks_lst):
                volunteer.save()
                for i in range(len(splits)):
                    split = round(splits[i], 4)
                    TimeSplit(time_donation=volunteer, time_split=split, task=tasks_lst[i]).save()
            else:
                form = TimeDonationForm()
                render(request, 'donations/volunteer.html', {'form': form})
            return HttpResponseRedirect('/donations/')
    else:
        form = TimeDonationForm()
    return render(request, 'donations/volunteer.html', {'form': form})