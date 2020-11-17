from django.contrib.auth import logout
from django.shortcuts import redirect, render
from donations.models import Level
from django.views import generic

class HomeView(generic.DetailView):
    model = Level
    template_name = 'google_login/index.html'

    def get_queryset(self):
        return Level.objects.filter(user=self.request.user)

def logout_request(request):
    logout(request)
    return redirect('https://project-1-34.herokuapp.com/')