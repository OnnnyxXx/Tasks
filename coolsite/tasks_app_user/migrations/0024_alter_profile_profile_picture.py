# Generated by Django 4.1.10 on 2023-08-26 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks_app_user', '0023_alter_profile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(upload_to='image/', verbose_name='Изображения'),
        ),
    ]
