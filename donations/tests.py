from django.contrib.auth.models import User
from django.test import TestCase

from .forms import MoneyDonationForm, TimeDonationForm, TaskForm
from . import views

class MoneyDonationFormTests(TestCase):
    def test_equivalence(self):
        form = MoneyDonationForm(data={'money_splits': '1.00'})
        self.assertTrue(form.is_valid())

class TimeDonationFormTests(TestCase):
    def test_equivalence(self):
        form = TimeDonationForm(data={'time_splits': '1'})
        self.assertTrue(form.is_valid())

class TaskFormTests(TestCase):
    def test_equivalence(self):
        form = TaskForm(data={'name': 'name', 'desc': 'desc', 'goal': '1'})
        self.assertTrue(form.is_valid())

    def test_boundary(self):
        form = TaskForm(data={'name': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'desc': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'goal': '1'})
        self.assertTrue(form.is_valid())

    def test_exception1(self):
        form = TaskForm(data={'name': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'desc': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'goal': '1'})
        self.assertFalse(form.is_valid())

    def test_exception2(self):
        form = TaskForm(data={'name': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'desc': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'goal': '1'})
        self.assertFalse(form.is_valid())

    def test_exception3(self):
        form = TaskForm(data={'name': '', 'desc': '', 'goal': ''})
        self.assertFalse(form.is_valid())

class process_splitsTests(TestCase):
    def test_equivalence1(self):
        splits, sum = views.process_splits('1.00')
        self.assertFalse(splits[0] > 1.00 or splits[0] < 1.00)

    def test_equivalence2(self):
        splits, sum = views.process_splits('1.00,2.00')
        self.assertFalse(splits[0] > 1.00 or splits[0] < 1.00)
        self.assertFalse(splits[1] > 2.00 or splits[1] < 2.00)

    def test_equivalence3(self):
        splits, sum = views.process_splits('1.00,2.00,3.00')
        self.assertFalse(splits[0] > 1.00 or splits[0] < 1.00)
        self.assertFalse(splits[1] > 2.00 or splits[1] < 2.00)
        self.assertFalse(splits[2] > 3.00 or splits[2] < 3.00)

    def test_boundary1(self):
        splits, sum = views.process_splits('0.01')
        self.assertFalse(splits[0] > 0.01 or splits[0] < 0.01)

    def test_boundary2(self):
        splits, sum = views.process_splits('999999999.99')
        self.assertFalse(splits[0] > 999999999.99 or splits[0] < 999999999.99)

    def test_boundary3(self):
        splits, sum = views.process_splits('0.01,999999999.98')
        self.assertFalse(splits[0] > 0.01 or splits[0] < 0.01)
        self.assertFalse(splits[1] > 999999999.98 or splits[1] < 999999999.98)

    def test_exception1(self):
        splits, sum = views.process_splits('0.00')
        self.assertTrue(splits[0] == -1)

    def test_exception2(self):
        splits, sum = views.process_splits('1000000000.00')
        self.assertTrue(splits[0] == -1)

    def test_exception3(self):
        splits, sum = views.process_splits('-1.00')
        self.assertTrue(splits[0] == -1)

    def test_exception4(self):
        splits, sum = views.process_splits('text')
        self.assertTrue(splits[0] == -1)