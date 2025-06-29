from django.db.models.signals import post_save, pre_delete, pre_save, post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.mail import mail_admins
from .models import Author, Profile
from Content.models import NewsReport, LatestNews


@receiver(post_save, sender=Author)
def create_profile(sender, instance, created, **kwargs):
    if created:
        mail_admins(
            subject="New Author Registration",
            message=f"A new author ({instance.user.username}) has registered and is awaiting approval."
        )
        Author.objects.create(user=instance)


@receiver(post_save, sender=Author)
def save_profile(sender, instance, **kwargs):
    if instance.author.save():
        mail_admins(
            subject="New User",
            message=f"Need to chck out the new user {instance.user.username}"
        )


@receiver(post_save, sender=NewsReport)
def notify_admin_new_report(sender, instance, created, **kwargs):
    if created:
        mail_admins(
            subject="New Report Submitted",
            message=f"A new report (ID: {instance.headline}) has been submitted by {instance.user.username} and is awaiting approval."
        )
        