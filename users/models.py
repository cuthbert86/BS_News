from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.contrib import admin
from django.dispatch import receiver


class Author(models.Model):
    username = models.OneToOneField(
        User, primary_key=True, max_length=30, on_delete=models.CASCADE,
        default='')
    name = models.CharField(max_length=30, default='')
    email = models.EmailField(max_length=100, default='')
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.username}'
