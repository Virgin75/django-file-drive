from django.views import View
from django.views.generic.edit import UpdateView
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth import get_user_model

from .forms import LoginForm, SignupForm
from .models import CustomUser

class LogInView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, "users/login.html", {'form': form})

    def post(self, request):
        # create a form instance and populate it with data from the request:
        form = LoginForm(data=request.POST)
        # check whether it's valid:
        if form.is_valid():
            user = authenticate(email=form.cleaned_data['username'], 
                        password=form.cleaned_data['password'])
            
            if user is not None:
                login(request, user)
                return redirect('/', user=user)
            else:
                #error cant login
                messages.add_message(request, messages.ERROR, 'Cannot login with the provided credentials.')
        messages.add_message(request, messages.ERROR, 'Form data is invalid.')
        return render(request, "users/login.html", {'form': form})



class SignUpView(View):

    def get(self, request):
        form = SignupForm()
        return render(request, "users/signup.html", {'form': form})

    def post(self, request):
        # create a form instance and populate it with data from the request:
        form = SignupForm(data=request.POST)
        # check whether it's valid:
        if form.is_valid():
            print(form.cleaned_data)
            user = get_user_model().objects.create_user(
                    email=form.cleaned_data['email'], 
                    password=form.cleaned_data['password1'])
           
            if user is not None:
                login(request, user)
                return redirect('/', user=user)

        messages.add_message(request, messages.ERROR, 'Form data is invalid.')
        return render(request, "users/signup.html", {'form': form})

class LogOutView(View):

    def get(self, request):
        logout(request)
        return render(request, 'users/loggedout.html')


class SettingsView(UpdateView):
    model = CustomUser
    fields = ['email', 'first_name', 'last_name']
    template_name = 'users/settings.html'

    def get_success_url(self):
        user_id = self.request.user.id
        redirect_to = f'/settings/{user_id}'
        messages.add_message(self.request, messages.SUCCESS, 'Profile updated successfully.')
        return redirect_to