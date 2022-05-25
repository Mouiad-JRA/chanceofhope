

from django.contrib import admin
from django.urls import path

from account.views import UserRegistrationView, LoginView, LogoutView

app_name = "account"
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('logout/', LogoutView.as_view(), name='user-logout'),
]
