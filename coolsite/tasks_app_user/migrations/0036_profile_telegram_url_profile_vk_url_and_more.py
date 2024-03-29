# Generated by Django 4.2.5 on 2023-09-11 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks_app_user', '0035_alter_profile_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='telegram_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='vk_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='youtube_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
