

from django.contrib import admin
from django.urls import path, include

from accounts.views import UserRegistrationView, LoginView, LogoutView, ChangePasswordView

app_name = "accounts"
urlpatterns = [
    path("accounts/", include("allauth.urls")),
    path("accounts/signup/", UserRegistrationView.as_view(), name="account_signup"),
    # path("profile/", view=UserDetailView.as_view(), name="profile"),
    # path("update-profile/", view=CandidateCreateView.as_view(), name="update_profile"),
    path("accounts/login/", view=LoginView.as_view(), name="account_login"),
    path("accounts/logout/", view=LogoutView.as_view(), name="account_logout"),
    path('accounts/reset-password/', ChangePasswordView.as_view(), name='reset-password'),

]
