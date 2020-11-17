from django.contrib.auth import logout
from django.shortcuts import render

def logout_request(request):
    logout(request)
    redirect(TemplateView.as_view(template_name="google_login/index.html"))