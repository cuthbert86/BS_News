from django.http import HttpResponse, HttpResponseNotFound
from .models import NewsReport, ContactSubmission, LatestNews
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic import DeleteView, FormView
from django.template.loader import get_template
from django.template import Context
import requests
from django.core.mail import send_mail
from users.models import Author, Profile
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import DeleteView, UpdateView
from .forms import NewsReportForm, ContactForm, EditNewsReportForm
from django.contrib.auth.models import User
from Complete_BS import settings
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import generic
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator
from rest_framework import viewsets
from .serializers import NewsSerializer
# from django.core.files.storage import FileSystemStorage
import logging


def home(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={},{}&units=metric&appid={}'
    cities = [('Sheffield', 'UK'), ('Melaka', 'Malaysia'), ('Bandung', 'Indonesia')]
    weather_data = []
    api_key = 'de13554a89154438878bf77424a0ca05'

    for city in cities:
        city_weather = requests.get(url.format(city[0], city[1], api_key)).json() # Request the API data and convert the JSON to Python data types

    weather = {
        'city': city_weather['name'] + ', ' + city_weather['sys']['country'],
        'temperature': city_weather['main']['temp'],
        'description': city_weather['weather'][0]['description']
    }
    weather_data.append(weather) # Add the data for the current city into our list

    return render(request, 'Content/home.html', {'title': 'Homepage', 'weather_data': weather_data})


def homepage(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={},{}&units=metric&appid={}'
    cities = [('Sheffield', 'UK'), ('Melaka', 'Malaysia'), ('Bandung', 'Indonesia')]
    weather_data = []
    api_key = 'de13554a89154438878bf77424a0ca05'

    for city in cities:
        city_weather = requests.get(url.format(city[0], city[1], api_key)).json() # Request the API data and convert the JSON to Python data types

    weather = {
        'city': city_weather['name'] + ', ' + city_weather['sys']['country'],
        'temperature': city_weather['main']['temp'],
        'description': city_weather['weather'][0]['description']
    }
    weather_data.append(weather) # Add the data for the current city into our list

    return render(request, 'Content/home.html', {'title': 'Homepage', 'weather_data': weather_data})


@login_required
def report_list(request):
    reports = NewsReport.objects.all()
    context = {'reports': reports}
    return render(request, 'Content/list_news.html', context)


class NewsReportDetail(DetailView):
    model = NewsReport
    fields = ['headline', 'todaysDate', 'author', 'content', 'photo']

    @login_required
    def news_report_detail(request, model):
        context = {NewsReport.objects.get()}
        if request.method != "POST":
            return HttpResponse("<h2>Method Not Allowed</h2>")
        else:
            NewsReport.headline = request.POST.get('headline')
            NewsReport.todaysDate = request.POST.get('todaysDate')
            NewsReport.content = request.POST.get('content')
            NewsReport.photo = request.POST.get('photo')
        return render(request, "Content/report_detail.html", context)


@login_required
def newsreport_detail(request, pk):
    report = get_object_or_404(NewsReport, pk=pk)
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        NewsReport.headline = request.POST.get('headline')
        NewsReport.todaysDate = request.POST.get('todaysDate')
        NewsReport.content = request.POST.get('content')
        NewsReport.photo = request.POST.get('photo')
        NewsReport.slug = request.Post.get('slug')
    return render(request, 'Content/report_detail', {'report': report})


@login_required
def latest_news_detail(request, pk):
    report = get_object_or_404(LatestNews, pk=pk)
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        LatestNews.title = request.POST.get('title')
        LatestNews.Date = request.POST.get('Date')
        LatestNews.content = request.POST.get('content')
        LatestNews.photo = request.POST.get('photo')
        LatestNews.slug = request.Post.get('slug')
    return render(request, 'Content/report_detail', {'report': report})


class EditNewsReportView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = NewsReport
    fields = [
            'headline',
            'content',
            'photo',
            'is_approved',
            'author',
            'todaysDate',
            'slug',
            ]

    @login_required
    def edit_report(self, form, request):
        if request.method == 'POST':
            form = EditNewsReportForm(request.POST or None)
        if form.is_valid():
            form.save()  # Save the module to the database
            return redirect(request, 'homepage')  # Redirect to the module list page or any other page
        else:
            form = EditNewsReportForm()

        return render(request, 'Content/edit_report.html', {'form': form})


def success_view(request):
    return render(request, 'Content/success.html')


@login_required
def create_report(request):
    if request.method == 'POST':
        form = NewsReportForm(request.POST, request.FILES)
        if form.is_valid():
            news_report = form.save(commit=True)
            news_report.author = request.usere  # Set author as current user
            # is_approved remains False by default
            news_report.save()
            return redirect('Content/homepage')  # Change to your homepage url name
    else:
        form = NewsReportForm()
    return render(request, 'Content/create_report.html', {'form': form})


def about_BS(request):
    return render(request, 'Content/about_BS.html',
                  {'title': 'Start Learning About BS News'})


def policies(request):
    return render(request, 'Content/policies.html',
                  {'title': 'BS News Offical Reporting Policies'})


class BSReportUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = NewsReport
    fields = ['headline', 'content', 'photo']
    success_url = 'Content/homepage'
    template_name = 'Content/create_news_report.html'

    @login_required
    def test_func2(self):
        newsreport = self.get_object()
        return self.request.user == newsreport.author


class BSReportDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = NewsReport
    form_class = NewsReportForm
    success_url = 'Content/homepage'

    @login_required
    def test_func3(self):
        newsreport = self.get_object()
        return self.request.user == newsreport.author


class ContactCreateView(CreateView, FormView):
    model = ContactSubmission
    form = ContactForm
    success_url = 'Content/success'
    template_name = 'Content/contact_create.html'

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'Unable to send the enquiry')
        return super().form_invalid(form)

    @login_required
    def get_success_url(self):
        return (self.request.path, 'Content/success.html')


class LatestNewsCreateView(CreateView, FormView):
    model = LatestNews
    form = NewsReportForm
    success_url = 'homepage'
    template_name = 'Content/create_report.html'

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'Unable to send the enquiry')
        return super().form_invalid(form)

    @login_required
    def get_success_url(self):
        return (self.request.path, 'homepage')


@login_required
def send_mail1(request):
    context = {}

    if request.method == 'POST':
        address = request.POST.get('address')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if address and subject and message:
            try:
                send_mail1(subject, message, settings.EMAIL_HOST_USER,
                           [address])
                context['result'] = 'Email sent successfully'
            except Exception as e:
                context['result'] = f'Error sending email: {e}'
        else:
            context['result'] = 'All fields are required'

    return render(request, "email.html", context)


@login_required
def report_detail(request, slug):
    # Filter posts based on the slug (case-insensitive)
    q = NewsReport.objects.filter(slug__iexact=slug)

    if q.exists():
        # If a post with the given slug exists, retrieve the first matching post
        q = q.first()
    else:
        # If no post is found, return an "Post Not Found" response
        return HttpResponse('<h1>Post Not Found</h1>')

    # Create a context dictionary containing the retrieved post
    context = {'NewsReport': q}

    # Render the 'details.html' template with the context
    return render(request, 'Content/report_detail.html', context)


class NewsViewSet(viewsets.ModelViewSet):
    queryset = NewsReport.objects.all()
    serializer_class = NewsSerializer


logger = logging.getLogger(__name__)


def my_view(request):
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")