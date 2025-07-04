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
from django.template.loader import get_template
from django.template import Context
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives


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

"""
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            
            return redirect('homepage')

        else:
            messages.warning(request, 'Unable to create account.')
    else:
        form = UserRegisterForm(UserCreationForm)
    return render(request, 'Content/register.html', {'form': form, 'title': 'Author Registration'})
"""


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            ######################### mail system #################################### 
            htmly = get_template('Content/Email.html')
            d = { 'username': username }
            subject, from_email, to = 'welcome', 'your_email@gmail.com', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            ################################################################## 
            messages.success(request, f'Your account has been created ! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'Content/register.html', {'form': form, 'title':'register here'})




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


class UserCreateView(CreateView, FormView):
    model = Author
    form = UserRegisterForm
    fields = ['username', 'name', 'email']
    context_object_name = 'user'
    success_url = 'success'
    template_name = 'Content/registration.html'

    def user_register(self, form, request):
        if request.method == 'POST':
            form = form(request.POST or None)
        if form.form_valid():
            form.save()  # Save the module to the database
            return redirect(request, 'homepage')  # Redirect to the module list page or any other page
        else:
            form = form()

        return render(request, 'Content/register.html', {'form': form})

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'Unable to send the enquiry')
        return super().form_invalid(form)

    @login_required
    def get_success_url(self):
        return (self.request.path, 'success')
    
    
