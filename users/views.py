from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Author
from .forms import UserRegisterForm
from .forms import LoginForm, UserUpdateForm
from django.contrib.auth import authenticate, login, logout
from django.db.models.signals import pre_save, post_save, post_migrate
from django.dispatch import receiver
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic import DeleteView, FormView
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse_lazy


def login_view(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

        # Check if a user with the provided username exists
        if not User.objects.filter(username=username).exists():
            # Display an error message if the username does not exist
            messages.error(request, 'Invalid Username')
            return redirect('LoginView')

        # Authenticate the user with the provided username and password
        username = authenticate(username=username, password=password)

        if username is None:
            # Display an error message if authentication fails (invalid password)
            messages.error(request, "Invalid Password")
            return redirect('LoginView')
        else:
            # Log in the user and redirect to the home page upon successful login
            login(request, username)
            return redirect('homepage')

    # Render the login page template (GET request)
    return render(request, 'Content/login.html')


def logout_view(request):
    logout(request)
    return redirect('homepage')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('itreporting:home')

        else:
            messages.warning(request, 'Unable to create account.')
    else:
        form = UserCreationForm()
    return render(request, 'Content/register.html', {'form': form, 'title': 'Registration'})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)

        if u_form.is_valid():
            u_form.save()
            messages.success(request, 'Your account has been successfully updated!')
            return redirect('profile')

        else:
            u_form = UserUpdateForm(instance=request.user)
            context = {'u_form': u_form, 'title': 'Profile'}

        return render(request, 'Content/profile.html', context)
