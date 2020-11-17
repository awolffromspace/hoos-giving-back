from django.urls import path

from . import views

app_name = 'google_login'
urlpatterns = [
    path('', TemplateView.as_view(template_name="google_login/index.html")),
    path('logout/', views.logout_request, name='logout'),
]