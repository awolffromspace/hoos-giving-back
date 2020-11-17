from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

def logout_request(request):
	logout(request)
	return HttpResponseRedirect(reverse(''))