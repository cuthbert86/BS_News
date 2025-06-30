from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Author
from .forms import UserUpdateForm, UserRegisterForm, ProfileUpdateForm
from .forms import NewPasswordChangeForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.db.models.signals import pre_save, post_save, post_migrate
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
        u_form = UserRegisterForm(request.POST)
        if u_form.is_valid():
            u_form.save()
            username = u_form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('homepage')

        else:
            messages.warning(request, 'Unable to create account.')
    else:
        form = UserRegisterForm(UserCreationForm)
    return render(request, 'Content/register.html', {'form': form, 'title': 'Author Registration'})


@receiver(post_save, sender=Author)
def created_author(sender, instance, created, **kwargs):
    if created:
        Author.objects.create(Username=instance)


@login_required
class PunterUpdateView(LoginRequiredMixin, UserPassesTestMixin,
                       UpdateView, FormView):

    model = Author
    form_class = ProfileUpdateForm
    fields = "__all__"
    context_object_name = 'user'
    template_name = "Content/register.html"

    @login_required
    def user_update(self, form, request):
        if request.method == 'POST':
            form = ProfileUpdateForm(request.POST or None)
        if form.is_valid():
            form.save()  # Save the module to the database
            return redirect(request, 'homepage')  # Redirect to the module list page or any other page
        else:
            form = ProfileUpdateForm()

        return render(request, 'Content/register.html', {'form': form})
