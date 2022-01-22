from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser


class LoginForm(AuthenticationForm):

    class Meta:
        model = CustomUser
        fields = ('email',)

class SignupForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email',)

class EditForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)