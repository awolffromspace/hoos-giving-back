from django.urls import path

from . import views

app_name = 'google_login'
urlpatterns = [
    path('', views.logout_request, name='logout'),
]