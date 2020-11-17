from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

def logout_request(request):
    logout(request)
    return redirect(TemplateView.as_view(template_name="google_login/index.html"))