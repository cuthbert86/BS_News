from django.contrib import admin
from django.urls import path, include, reverse_lazy, re_path, reverse
from users import views as user_views
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from Content.views import NewsReportDetail, homepage, report_detail
from Content.views import success, NewsReportDetail, send_mail1
from Content.views import BSReportDeleteView, BSReportUpdateView, about_BS
from Content.views import ContactCreateView, create_report, report_list
from Content.views import EditNewsReportView, NewsViewSet
from Content import views
from Content.models import NewsReport
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin


app_name = "Content"

router = DefaultRouter()
router.register(r'NewsReport', NewsViewSet)


urlpatterns = [
    path('Content/homepage', homepage, name='homepage'),
    path('Content/success', success, name='success'),
    path('Content/about_BS', about_BS, name='about_BS'),
    path('Content/BS_delete_report', BSReportDeleteView.as_view(
        template_name='BS_delete_report.html'), name='BS_delete_report'),
    path('Content/contact_create', ContactCreateView.as_view(
        template_name='contact_create.html'), name='contact_create'),
    path('Content/create_report', create_report, name='create_report'),
    path('Content/report_list', report_list, name='report_list'),
    path("Content/<slug:slug>/", NewsReportDetail,
         name="news_report_detail"),
    path('', include(router.urls)),
    path('Content/send_mail1', send_mail1, name='email'),
    path('Content/EditNewsReportView', EditNewsReportView.as_view(
        template_name='edit_report.html'), name='edit_report'),
    re_path('Content/<slug:slug>/', report_detail, name='report_detail'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
