from django.contrib import admin
from .models import NewsReport, ContactSubmission, LatestNews

admin.site.register(NewsReport)
admin.site.register(ContactSubmission)
admin.site.register(LatestNews)
