from django.urls import path
from .views import LogInView, SignUpView, LogOutView, SettingsView

urlpatterns = [
    path('login', LogInView.as_view(), name="loginview"),
    path('signup', SignUpView.as_view(), name="signupview"),
    path('logout', LogOutView.as_view(), name="logoutview"),
    path('settings/<pk>', SettingsView.as_view(), name="settingsview"),
]