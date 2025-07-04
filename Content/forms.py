from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import NewsReport, ContactSubmission
from django.contrib.auth.decorators import login_required
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from django.utils import timezone
from users.models import Author
from django.core.mail import send_mail


@login_required
class EditNewsReportForm(forms.ModelForm):
    model = NewsReport
    fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout()
        Fieldset(
            'headline',
            'content',
            'photo',
            'is_approved',
            'author',
            'todaysDate'
            'slug'
            ),
        Submit('submit', 'Submit', css_class='button white')


class ContactForm(forms.ModelForm):
    model = ContactSubmission
    fields = ['subject', 'name', 'message', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout()
        Fieldset(
            'subject',
            'name',
            'message',
            'email',
            ),
        Submit('submit', 'Submit', css_class='button white')


class NewsReportForm(forms.ModelForm):
    class Meta:
        model = NewsReport
        fields = ['headline', 'content', 'photo']
