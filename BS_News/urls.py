from django.contrib import admin
from django.urls import path, include, reverse_lazy, re_path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from BS_News import views as BS_views
from BS_News.urls import urlpatterns as urls
from BS_News.views import live_feed, report, archive


urlpatterns = [
    
]
