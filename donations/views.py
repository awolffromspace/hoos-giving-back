from django.shortcuts import render

from .models import MoneyDonation, TimeDonation

class IndexView(generic.ListView):
    template_name = 'donations/index.html'
    context_object_name = 'donation_list'

    def get_queryset(self):
    	time_donations = TimeDonation.objects.filter(
            user=request.user
        )
        money_donations = MoneyDonation.objects.filter(
            user=request.user
        )
        both_donations = money_donations | time_donations
        return both_donations.order_by('-date_donated')