from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.contrib import admin
from django.dispatch import receiver
from django.contrib.auth import get_user_model


class Author(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        max_length=30,
        default='user_name')
    first_name = models.CharField(max_length=10, default='')
    last_name = models.CharField(max_length=10, default='')
    email = models.EmailField(max_length=100, default='')
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.first_name} + {self.user.last_name}'
