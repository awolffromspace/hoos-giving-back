# /***************************************************************************************
# *  REFERENCES
# *  Title: In 5 Mins: Set up Google Login to Sign up Users on Django
# *  Author: Zoe Chew
# *  Date: 7/27/19
# *  Code version: N/A
# *  URL: https://whizzoe.medium.com/in-5-mins-set-up-google-login-to-sign-up-users-on-django-e71d5c38f5d5
# *  Software License: N/A
# ***************************************************************************************/

"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from google_login import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('logout/', views.logout_request, name='logout'),
    path('donations/', include('donations.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
]
