from django.contrib.auth import logout
from django.shortcuts import redirect, render
from donations.models import Level

def homepage(request):
    level = Level.objects.filter(user=self.request.user)
    return render(request, 'google_login/index.html', {'level': level})

def logout_request(request):
    logout(request)
    return redirect('https://project-1-34.herokuapp.com/')