from datetime import timedelta
from django.contrib.auth.models import User
from django.test import TestCase

from .forms import MoneyDonationForm, TimeDonationForm

class MoneyDonationFormTests(TestCase):
    def test_equivalence(self):
        form = MoneyDonationForm(data={'money_total': 1.00})
        self.assertTrue(form.is_valid())

    def test_boundary1(self):
        form = MoneyDonationForm(data={'money_total': 0.01})
        self.assertTrue(form.is_valid())

    def test_boundary2(self):
        form = MoneyDonationForm(data={'money_total': 999999.99})
        self.assertTrue(form.is_valid())

    # TODO: Figure out how to perform exception tests on forms
    # def test_exception1(self):
    #     form = MoneyDonationForm(data={'money_total': 0.00})
    #     self.assertFalse(form.is_valid())

    # def test_exception2(self):
    #     form = MoneyDonationForm(data={'money_total': 1000000.00})
    #     self.assertFalse(form.is_valid())

class TimeDonationFormTests(TestCase):
    def test_equivalence(self):
        form = TimeDonationForm(data={'time_total': timedelta(hours=1)})
        self.assertTrue(form.is_valid())

    def test_boundary1(self):
        form = TimeDonationForm(data={'time_total': timedelta(seconds=1)})
        self.assertTrue(form.is_valid())

    def test_boundary2(self):
        form = TimeDonationForm(data={'time_total': timedelta.max})
        self.assertTrue(form.is_valid())

    # def test_exception(self):
    #     form = TimeDonationForm(data={'time_total': timedelta(seconds=-1)})
    #     self.assertFalse(form.is_valid())