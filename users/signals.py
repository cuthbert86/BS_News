from django.db.models.signals import post_save, pre_delete
from django.db.models.signals import pre_save, post_save, post_migrate
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.mail import mail_admins
from .models import Author
from Content.models import NewsReport, LatestNews
from django.contrib.auth import get_user_model


"""
@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    Author = get_user_model()
    if not Author.objects.filter(username='CuthbertBaines').exists():
        Author.objects.create_superuser(
            'CuthbertBaines', 'cuthbert.corp@gmail.com', 'Burngreave1986')
"""


@receiver(post_save, sender=Author)
def create_profile(sender, instance, created, **kwargs):
    if created:
        mail_admins(
            subject="New Author Registration",
            message=f"A new author ({instance.username}) has registered and is awaiting approval."
        )
        Author.objects.create(User=instance)


@receiver(post_save, sender=Author)
def save_profile(sender, instance, created, **kwargs):
    if created:
        mail_admins(
            subject="New User",
            message=f"Need to check out the new user {instance.username}"
        )


@receiver(post_save, sender=NewsReport)
def notify_admin_new_report(sender, instance, created, **kwargs):
    if created:
        mail_admins(
            subject="New Report Submitted",
            message=f"A new report (ID: {instance.slug}) has been submitted by {instance.username} and is awaiting approval."
        )
