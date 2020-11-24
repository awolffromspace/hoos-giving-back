# /***************************************************************************************
# *  REFERENCES
# *  Title: Django Stripe Payments Simplified With Donation Page
# *  Author: Dennis Ivy
# *  Date: 3/13/20
# *  Code version: N/A
# *  URL: https://www.youtube.com/watch?v=oZwyA9lUwRk
# *  Software License: N/A
# *
# *  Title: Stripe API Reference
# *  Author: N/A
# *  Date: 11/13/20
# *  Code version: N/A
# *  URL: https://stripe.com/docs/api
# *  Software License: N/A
# ***************************************************************************************/

import stripe

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.views import generic
from itertools import chain
from operator import attrgetter

from .forms import MoneyDonationForm, TimeDonationForm, TaskForm
from .models import Charity, Task, MoneyDonation, TimeDonation, Level

stripe.api_key = 'sk_test_51Hmsn6A6a6h8LgDy02KZ3YjlftIk89TbokiSyGJ2GPGZ6LUN4bFFnpBMa2ONGXwH4U09yxy4KIdpd9G6MF7ATWkh007YmN3paT'

class IndexView(generic.ListView):
    template_name = 'donations/index.html'
    context_object_name = 'donation_list'

    def get_queryset(self):
        all_donations = MoneyDonation.objects.none()
        money_donations = MoneyDonation.objects.all()
        time_donations = TimeDonation.objects.all()
        all_donations = sorted(
            chain(money_donations, time_donations),
            key=attrgetter('date_donated'),
            reverse=True
        )
        return all_donations

def process_splits(splits_str):
    if splits_str.endswith(','):
        splits_str = splits_str[0 : len(splits_str) - 1]
    splits_strlst = splits_str.split(',')
    splits = []
    sum = 0
    for i in range(len(splits_strlst)):
        try:
            split = float(splits_strlst[i])
            if split < 0.00:
                return [-1], sum
            splits.append(split)
            sum += split
        except ValueError:
            return [-1], sum
    if sum < 0.50 or sum > 999999999.99:
        return [-1], sum
    return splits, sum

def update_level(user):
    if user.is_authenticated:
        level = Level.objects.filter(
            user=user
        )
        money_sum = 0
        time_sum = 0
        money_donations = MoneyDonation.objects.filter(
            user=user
        )
        time_donations = TimeDonation.objects.filter(
            user=user
        )
        for donation in money_donations:
            money_sum = money_sum + float(donation.money_total)
        for donation in time_donations:
            time_sum = time_sum + donation.time_total
        value = 1 + int(money_sum / 10 + time_sum / 30)
        if not level:
            Level(user=user, value=value).save()
        else:
            level.update(value=value)

def donate(request):
    charities = Charity.objects.all()
    if request.method == 'POST':
        form = MoneyDonationForm(request.POST)
        if form.is_valid():
            splits, sum = process_splits(form.cleaned_data['money_splits'])
            if splits[0] > -1:
                request.session['donation_splits'] = splits
                request.session['donation_total'] = sum
                return HttpResponseRedirect('/donations/pay/')
            else:
                form = MoneyDonationForm()
                return render(request, 'donations/donate.html', {'form': form, 'charity_list': charities})
    else:
        form = MoneyDonationForm()
    return render(request, 'donations/donate.html', {'form': form, 'charity_list': charities})

def volunteer(request):
    tasks = Task.objects.filter(fulfilled=False)
    if request.method == 'POST':
        form = TimeDonationForm(request.POST)
        if form.is_valid():
            splits, sum = process_splits(form.cleaned_data['time_splits'])
            if splits[0] > -1:
                index = 0
                for task in tasks:
                    split = int(splits[index])
                    if split > 0:
                        updated_goal = task.goal - split
                        if (updated_goal <= 0):
                            updated_goal = 0
                            task.fulfilled = True
                            split = task.goal
                        task.goal = updated_goal
                        task.save()
                        TimeDonation(user=request.user, date_donated=timezone.now(), time_total=split, task=task).save()
                    index += 1
                update_level(request.user)
                return HttpResponseRedirect('/donations/')
            else:
                form = TimeDonationForm()
                return render(request, 'donations/volunteer.html', {'form': form, 'task_list': tasks})
    else:
        form = TimeDonationForm()
    return render(request, 'donations/volunteer.html', {'form': form, 'task_list': tasks})

def submit_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            try:
                goal = int(form.cleaned_data['goal'])
                Task(user=request.user, name=form.cleaned_data['name'], desc=form.cleaned_data['desc'], goal=goal).save()
                return HttpResponseRedirect('/donations/volunteer/')
            except:
                return render(request, 'donations/task.html', {'form': form})
    else:
        form = TaskForm()
    return render(request, 'donations/task.html', {'form': form})

def pay(request):
    amount = 0
    if 'donation_total' in request.session and 'donation_splits' in request.session:
        amount = int(float(request.session['donation_total']) * 100)
        if amount < 0.50:
            return render(request, 'donations/pay.html')
    else:
        return render(request, 'donations/pay.html')
    
    if request.method == 'POST':
        customer = stripe.Customer.create(
            name=request.user.first_name + ' ' + request.user.last_name,
            email=request.user.email,
            source=request.POST['stripeToken']
        )

        charge = stripe.Charge.create(
            customer=customer,
            amount=amount,
            currency='usd',
            description='Donation'
        )

        charities = Charity.objects.all()
        splits = request.session['donation_splits']
        index = 0
        for charity in charities:
            split = splits[index]
            if split > 0.00:
                MoneyDonation(user=request.user, date_donated=timezone.now(), money_total=split, charity=charity).save()
            index += 1
        update_level(request.user)

        return HttpResponseRedirect('/donations/')

    return render(request, 'donations/pay.html')
