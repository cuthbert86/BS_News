from django.db import models
from django.db.models import Model
from django.contrib.auth.models import User
from users.models import Profile, Author
from datetime import datetime
from django.conf import settings
from rest_framework import serializers
from django.urls import reverse
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from Complete_BS.utils import unique_slug_generator, unique_slug_generator1
import os


class NewsReport(models.Model):
    headline = models.TextField(primary_key=True, max_length=100, default='')
    todaysDate = models.DateTimeField(
        auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,)
    content = models.TextField(max_length=500, default='')
    photo = models.ImageField(upload_to='media/photo', default='busgate.jpg')
    is_approved = models.BooleanField(default=True)
    slug = models.SlugField(max_length=100, null=True, blank=True)

    def publish(self):
        self.todaysDate = datetime.now()
        self.save()

    def get_absolute_url(self):
        return reverse('Content/report_detail', kwargs={"slug": self.slug})

    class Meta:
        get_latest_by = "todaysDate"


@receiver(pre_save, sender=NewsReport)
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


class LatestNews(models.Model):
    title = models.CharField(primary_key=True, max_length=80, default='')
    Date = models.DateField(auto_now_add=True)
    reporter = models.ForeignKey(
        Profile, related_name='username', on_delete=models.CASCADE)
    content = models.TextField(max_length=500, default='')
    photo = models.ImageField(upload_to='media/photo', default='busgate.jpg')
    is_approved = models.BooleanField(default=True)
    slug = models.SlugField(max_length=100, null=True, blank=True, unique=True)

    def publish(self):
        self.Date = datetime.now()
        self.save()

    def __str__(self):
        return f'{self.title}'

    class Meta:
        get_latest_by = "Date"


@receiver(pre_save, sender=LatestNews)
def pre_save_receiver1(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator1(instance)


class ContactSubmission(models.Model):
    Date = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=20, default='N/A')
    email = models.EmailField(max_length=50, default='')
    subject = models.CharField(max_length=50, default='')
    message = models.TextField(max_length=300, default='')

    def __str__(self):
        return f'{self.Date} - {self.subject}'
