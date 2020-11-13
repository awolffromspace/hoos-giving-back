import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.views import generic
from itertools import chain
from operator import attrgetter

from .forms import MoneyDonationForm, TimeDonationForm
from .models import MoneyDonation, TimeDonation

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
            charities = ['The Trevor Project', 'The National Immigration Law Center', 'Human Rights Watch', 'The Global Fund for Women', 'Charity Water', 'Mental Health America']
            if splits[0] > -1 and len(splits) == len(charities):
                donation.save()
                for i in range(len(splits)):
                    if split > 0.00:
                        MoneyDonation(user=request.user, date_donated=timezone.now(), money_total=split, charity=charities[i]).save()
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
            tasks = form.cleaned_data['tasks']
            tasks_lst = tasks.split(',')
            if splits[0] > -1 and len(splits) == len(tasks_lst):
                volunteer.save()
                for i in range(len(splits)):
                    TimeDonation(user=request.user, date_donated=timezone.now(), time_total=split, task=tasks_lst[i])
            else:
                form = TimeDonationForm()
                render(request, 'donations/volunteer.html', {'form': form})
            return HttpResponseRedirect('/donations/')
    else:
        form = TimeDonationForm()
    return render(request, 'donations/volunteer.html', {'form': form})