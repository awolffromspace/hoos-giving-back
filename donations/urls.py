from django.urls import path

from . import views

app_name = 'donations'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('donate/', views.donate, name='donate'),
    path('volunteer/', views.volunteer, name='volunteer'),
    path('pay/', views.pay, name='pay'),
]
