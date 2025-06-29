from django.contrib import admin
from .models import Author, Profile
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class UserModel(UserAdmin):
    pass


admin.site.register(Author)
admin.site.register(Profile)
