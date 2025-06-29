from django.db import models
from django.db.models import Model
from django.contrib.auth.models import User
from datetime import datetime, date
from django.utils import timezone
from django.conf import settings
# from rest_framework import serializers
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from PIL import Image

# Create your models here.


class Report(models.Model):
    headline = models.CharField(primary_key=True, max_length=100, default='')
    todaysDate = models.DateField(auto_now_add=True)
    author = (models.ForeignKey(
        User, related_name='user', on_delete=models.CASCADE))
    content = models.TextField(max_length=500, default='')
    photo = models.ImageField(upload_to='media/photos/', blank=True)
    is_approved = models.BooleanField(default=False)  # New field

    def publish(self):
        self.todaysDate = datetime.now()
        self.save()
    