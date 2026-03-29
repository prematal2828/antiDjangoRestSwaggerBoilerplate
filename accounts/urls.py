"""
URL patterns for the accounts app.
"""

from django.urls import path

from .views import ChangePasswordView, LoginView, LogoutView, RegisterView, TokenRefreshView, UserProfileView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="auth-register"),
    path("login/", LoginView.as_view(), name="auth-login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="auth-token-refresh"),
    path("logout/", LogoutView.as_view(), name="auth-logout"),
    path("profile/", UserProfileView.as_view(), name="auth-profile"),
    path("password/change/", ChangePasswordView.as_view(), name="auth-password-change"),
]
