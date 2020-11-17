from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

def logout_request(request):
    logout(request)
    redirect('https://project-1-34.herokuapp.com/')