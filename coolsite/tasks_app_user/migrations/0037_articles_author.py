# Generated by Django 4.2.5 on 2023-09-20 12:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks_app_user', '0036_profile_telegram_url_profile_vk_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='articles',
            name='author',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
