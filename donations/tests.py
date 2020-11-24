from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from .forms import MoneyDonationForm, TimeDonationForm, TaskForm
from .models import Charity, Task, MoneyDonation, TimeDonation, Level
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

class UpdateLevelTests(TestCase):
    def test_equivalence1(self):
        self.user = User.objects.create_user(username='test', password='test')
        views.update_level(self.user)
        level = Level.objects.filter(user=self.user).first().value
        self.assertTrue(level == 1)

    def test_equivalence2(self):
        self.user = User.objects.create_user(username='test', password='test')
        charity = Charity(name="Charity Name", desc="Charity Description")
        charity.save()
        MoneyDonation(user=self.user, date_donated=timezone.now(), money_total=15.00, charity=charity).save()
        task = Task(name="Task Name", desc="Task Description", goal=60)
        task.save()
        TimeDonation(user=self.user, date_donated=timezone.now(), time_total=40, task=task).save()
        views.update_level(self.user)
        level = Level.objects.filter(user=self.user).first().value
        self.assertTrue(level == 3)

    def test_boundary1(self):
        self.user = User.objects.create_user(username='test', password='test')
        charity = Charity(name="Charity Name", desc="Charity Description")
        charity.save()
        MoneyDonation(user=self.user, date_donated=timezone.now(), money_total=9.99, charity=charity).save()
        views.update_level(self.user)
        level = Level.objects.filter(user=self.user).first().value
        self.assertTrue(level == 1)

    def test_boundary2(self):
        self.user = User.objects.create_user(username='test', password='test')
        charity = Charity(name="Charity Name", desc="Charity Description")
        charity.save()
        MoneyDonation(user=self.user, date_donated=timezone.now(), money_total=10.00, charity=charity).save()
        views.update_level(self.user)
        level = Level.objects.filter(user=self.user).first().value
        self.assertTrue(level == 2)

    def test_boundary3(self):
        self.user = User.objects.create_user(username='test', password='test')
        task = Task(name="Task Name", desc="Task Description", goal=60)
        task.save()
        TimeDonation(user=self.user, date_donated=timezone.now(), time_total=29, task=task).save()
        views.update_level(self.user)
        level = Level.objects.filter(user=self.user).first().value
        self.assertTrue(level == 1)

    def test_boundary4(self):
        self.user = User.objects.create_user(username='test', password='test')
        task = Task(name="Task Name", desc="Task Description", goal=60)
        task.save()
        TimeDonation(user=self.user, date_donated=timezone.now(), time_total=30, task=task).save()
        views.update_level(self.user)
        level = Level.objects.filter(user=self.user).first().value
        self.assertTrue(level == 2)

class ProcessSplitsTests(TestCase):
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
        splits, sum = views.process_splits('0.50')
        self.assertFalse(splits[0] > 0.50 or splits[0] < 0.50)

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
        splits, sum = views.process_splits('0.49')
        self.assertTrue(splits[0] == -1)

    def test_exception3(self):
        splits, sum = views.process_splits('1000000000.00')
        self.assertTrue(splits[0] == -1)

    def test_exception4(self):
        splits, sum = views.process_splits('-1.00')
        self.assertTrue(splits[0] == -1)

    def test_exception5(self):
        splits, sum = views.process_splits('text')
        self.assertTrue(splits[0] == -1)