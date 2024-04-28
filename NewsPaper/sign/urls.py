from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import BaseRegisterView, upgrade_me

urlpatterns = [
    path('sign/login/',
         LoginView.as_view(template_name='sign/login.html'),
         name='login'),
    path('sign/logout/',
         LogoutView.as_view(template_name='sign/logout.html'),
         name='logout'),
    path('sign/signup/',
         BaseRegisterView.as_view(template_name='sign/signup.html'),
         name='signup'),
    path('accounts/upgrade/', upgrade_me, name='upgrade'),
]
