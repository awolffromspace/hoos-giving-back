import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.views import generic
from itertools import chain
from operator import attrgetter

from .forms import MoneyDonationForm, TimeDonationForm
from .models import MoneyDonation, TimeDonation

import stripe

stripe.api_key = "sk_test_51Hmsn6A6a6h8LgDy02KZ3YjlftIk89TbokiSyGJ2GPGZ6LUN4bFFnpBMa2ONGXwH4U09yxy4KIdpd9G6MF7ATWkh007YmN3paT"

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
            money_donation = MoneyDonation(user=request.user, date_donated=timezone.now(), money_total=form.cleaned_data['money_total'])
            money_donation.save()
            return HttpResponseRedirect('/donations/pay/')
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

def pay(request):

    '''
    How to fix me:
    - Need to somehow take in donation amount from last page
    - Need to have a name/email for customer (a string)... unsure how to get it using google login
    - The donation should not be recorded on the app until after payment is given
    '''


    amount = 1
   
    
    if request.method == 'POST':

        
        customer = stripe.Customer.create(
                name= self.request.user.username,
                source=request.POST['stripeToken']
            )

#charge = stripe.Charge.create(
#                customer=customer,
#amount = 5
#                currency = "usd",
#                description = "Donation"
#                )

        return HttpResponseRedirect('/donations/')

    return render(request, 'donations/pay.html')

