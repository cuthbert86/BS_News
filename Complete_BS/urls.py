"""
URL configuration for Complete_BS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, reverse_lazy, re_path
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from Content import views as Content_views
# from Content.views import send_mail
# from BS_News import views as BS_news
# from BS_News.urls import urlpatterns as urls
# from users.forms import NewPasswordChangeForm
from Content.urls import urlpatterns as urls
# from Content import forms
from Content.views import home, homepage, policies


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('homepage', homepage, name='homepage'),
    path('policies', policies, name='policies'),
    path('/', include('Content.urls')),
#    path('__debug__/', include('debug_toolbar.urls')),
    path('users/register', user_views.register, name='register'),
 #   path('users/profile', user_views.profile, name='profile'),
    path('users/register_profile', user_views.register_profile,
         name='register_profile'),
#    path('users/logout_view', user_views.logout_view, name='logout'),
    path('login',
         auth_views.LoginView.as_view(template_name='Content/login.html'),
         name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(template_name='Content/logout.html'),
         name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)