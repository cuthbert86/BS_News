from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from .models import Author


class CustomUserCreationForm(AdminUserCreationForm):
    class Meta:
        model = Author
        fields = ("first_name", "last_name", "email")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Author
        fields = ("first_name", "last_name", "email")


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email address',
                             help_text='Your SHU email address.')

    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email']


class NewPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
