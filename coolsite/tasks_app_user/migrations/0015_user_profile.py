# Generated by Django 4.1.10 on 2023-08-23 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks_app_user', '0014_delete_user_messnegr'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_user', models.CharField(max_length=25, verbose_name='Ваше Имя')),
                ('sity_user', models.CharField(max_length=23, verbose_name='Ваш Город')),
                ('email_user', models.CharField(max_length=35, verbose_name='Email')),
            ],
        ),
    ]
