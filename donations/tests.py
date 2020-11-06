from datetime import timedelta
from decimal import *
from django.contrib.auth.models import User
from django.test import TestCase

from .forms import MoneyDonationForm, TimeDonationForm
from . import views

class MoneyDonationFormTests(TestCase):
    def test_equivalence(self):
        form = MoneyDonationForm(data={'money_total': Decimal('1.00'), 'money_splits': '1.0'})
        self.assertTrue(form.is_valid())

    def test_boundary1(self):
        form = MoneyDonationForm(data={'money_total': Decimal('0.01'), 'money_splits': '1.0'})
        self.assertTrue(form.is_valid())

    def test_boundary2(self):
        form = MoneyDonationForm(data={'money_total': Decimal('999999.99'), 'money_splits': '1.0'})
        self.assertTrue(form.is_valid())

    def test_exception1(self):
        form = MoneyDonationForm(data={'money_total': Decimal('0.00'), 'money_splits': '1.0'})
        self.assertEqual(
            form.errors['money_total'], ['Ensure this value is greater than or equal to 0.01.']
        )

    def test_exception2(self):
        form = MoneyDonationForm(data={'money_total': Decimal('1000000.00'), 'money_splits': '1.0'})
        self.assertEqual(
            form.errors['money_total'], ['Ensure that there are no more than 8 digits in total.']
        )
  

class TimeDonationFormTests(TestCase):
    def test_equivalence(self):
        form = TimeDonationForm(data={'time_total': timedelta(hours=1), 'time_splits': '1.0'})
        self.assertTrue(form.is_valid())

    def test_boundary1(self):
        form = TimeDonationForm(data={'time_total': timedelta(seconds=1), 'time_splits': '1.0'})
        self.assertTrue(form.is_valid())

    def test_boundary2(self):
        form = TimeDonationForm(data={'time_total': timedelta.max, 'time_splits': '1.0'})
        self.assertTrue(form.is_valid())

    def test_exception(self):
        form = TimeDonationForm(data={'time_total': timedelta(seconds=-1), 'time_splits': '1.0'})
        self.assertEqual(
            form.errors['time_total'], ['Ensure this value is positive.']
        )

class ProcessSplitsTests(TestCase):
    def test_equivalence1(self):
        splits = processSplits('0.50,0.50')
        for i in splits:
            self.assertFalse(i > 0.50 or i < 0.50)

    def test_equivalence2(self):
        splits = processSplits('0.49,0.50')
        self.assertFalse(splits[0] > 0.495 or splits[0] < 0.495)
        self.assertFalse(splits[1] > 0.505 or splits[1] < 0.505)

    def test_equivalence3(self):
        splits = processSplits('0.33,0.33,0.33')
        for i in splits:
            self.assertFalse(i > 0.3334 or i < 0.3334)

    def test_boundary1(self):
        splits = processSplits('0.0,0.99')
        self.assertFalse(splits[0] > 0.5 or splits[0] < 0.5)
        self.assertFalse(splits[1] > 0.995 or splits[1] < 0.995)

    def test_boundary2(self):
        splits = processSplits('0.01,0.98')
        self.assertFalse(splits[0] > 0.015 or splits[0] < 0.015)
        self.assertFalse(splits[1] > 0.985 or splits[1] < 0.985)

    def test_boundary2(self):
        splits = processSplits('0.99')
        self.assertFalse(splits[0] > 1.00 or splits[0] < 1.00)

    def test_exception1(self):
        splits = processSplits('0.49,0.49')
        self.assertTrue(splits[0] == -1)

    def test_exception2(self):
        splits = processSplits('0.0,0.98')
        self.assertTrue(splits[0] == -1)

    def test_exception3(self):
        splits = processSplits('0.0')
        self.assertTrue(splits[0] == -1)

    def test_exception4(self):
        splits = processSplits('1.01')
        self.assertTrue(splits[0] == -1)