from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm
from .models import Author, Profile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        label='Username',
        help_text='This will be the name that is attached to your reports so use a pen name if you want')
    name = forms.CharField(label='Second Name',
                           help_text='Please Enter your name you normally use')
    email = forms.EmailField(label='Email address',
                             help_text='A fake one should be OK')

    class Meta:
        model = User
        fields = ['username', 'name', 'password1', 'password2']


class NewPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True


class ProfileUpdateForm(UserCreationForm):
    username = forms.CharField(
        label='Name',
        help_text='Please Enter your name you normally use')

    class Meta:
        model = Author
        fields = "__all__"


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(
        label='Username',
        help_text='This will be the name that is attached to your reports so use a pen name if you want')
    email = forms.EmailField(label='Email address',
                             help_text='A fake one will be OK')

    class Meta:
        model = User
        fields = "__all__"


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class ProfileRegisterForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = ['reporter', 'name', 'email', 'password1', 'password2']


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"


class ProfileLoginForm(forms.Form):
    reporter = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))