from datetime import timedelta
from decimal import *
from django.contrib.auth.models import User
from django.test import TestCase

from .forms import MoneyDonationForm, TimeDonationForm

class MoneyDonationFormTests(TestCase):
    def test_equivalence(self):
        form = MoneyDonationForm(data={'money_total': Decimal('1.00')})
        self.assertTrue(form.is_valid())

    def test_boundary1(self):
        form = MoneyDonationForm(data={'money_total': Decimal('0.01')})
        self.assertTrue(form.is_valid())

    def test_boundary2(self):
        form = MoneyDonationForm(data={'money_total': Decimal('999999.99')})
        self.assertTrue(form.is_valid())

    def test_exception1(self):
        form = MoneyDonationForm(data={'money_total': Decimal('0.00')})
        self.assertEqual(
            form.errors['money_total'], ['Ensure this value is greater than or equal to 0.01.']
        )

    def test_exception2(self):
        form = MoneyDonationForm(data={'money_total': Decimal('1000000.00')})
        self.assertEqual(
            form.errors['money_total'], ['Ensure that there are no more than 8 digits in total.']
        )

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

    def test_exception(self):
        form = TimeDonationForm(data={'time_total': timedelta(seconds=-1)})
        self.assertEqual(
            form.errors['time_total'], ['Ensure this value is positive.']
        )