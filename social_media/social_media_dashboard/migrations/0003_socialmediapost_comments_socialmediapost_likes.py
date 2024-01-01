# Generated by Django 4.2.5 on 2023-12-28 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_media_dashboard', '0002_socialmediapost_userprofile_facebook_access_token_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialmediapost',
            name='comments',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='socialmediapost',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
