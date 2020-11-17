from django.contrib.auth import logout
from django.shortcuts import redirect, render

def logout_request(request):
    logout(request)
    return redirect('https://project-1-34.herokuapp.com/')