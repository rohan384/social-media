from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
# social_media_dashboard/models.py

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    twitter_access_token = models.CharField(max_length=255, blank=True, null=True)
    twitter_access_token_secret = models.CharField(max_length=255, blank=True, null=True)
    facebook_access_token = models.CharField(max_length=255, blank=True, null=True)
    # Add other profile fields
    def __str__(self):
        return self.user.username

class SocialMediaPost(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    platform = models.CharField(max_length=50)  # e.g., Twitter, Facebook
    post_text = models.TextField()
    likes = models.IntegerField(default=0)
    comments = models.TextField(blank=True, null=True)
    # Add other post fields

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()