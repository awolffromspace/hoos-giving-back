from django.contrib.auth.models import User
from django.test import TestCase

from .models import MoneyDonation, TimeDonation

class MoneyDonationModelTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user('Test User', 'test@email.com', 'testpswd')

	def tearDown(self):
		self.user.delete()