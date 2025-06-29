from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Author, User, Profile
from .forms import UserUpdateForm, ProfileUpdateForm, UserRegisterForm, UpdateForm
from .forms import NewPasswordChangeForm, LoginForm, ProfileLoginForm, ProfileRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic import DeleteView, FormView
from django.http import HttpResponse


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
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('Content/homepage')

        else:
            messages.warning(request, 'Unable to create account.')
    else:
        form = UserRegisterForm(UserCreationForm)
    return render(request, 'Content/register.html', {'form': form, 'title': 'Author Registration'})


@login_required
def register_profile(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST, instance=request.username)
        p_form = ProfileRegisterForm(
            request.POST, request.FILES, instance=request.profile)

        if form.is_valid() and p_form.is_valid():
            form.save()
            p_form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
        else:
            messages.warning(request, 'Unable to create account.')
    else:
        form = ProfileRegisterForm(UserCreationForm)
    return render(request, 'Content/register.html', {'form': form, 'title': 'Author Registration'})


@receiver(post_save, sender=Profile)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
