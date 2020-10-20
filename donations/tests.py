from django.contrib.auth.models import User
from django.test import TestCase

from .forms import MoneyDonationForm, TimeDonationForm

class MoneyDonationFormTests(TestCase):
	def test_equivalence(self):
		form = MoneyDonationForm(data={'money_total': 2})
		self.assertTrue(form.is_valid())