# Generated by Django 4.2.6 on 2023-10-12 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks_app_user', '0047_category_articles_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='categories/'),
        ),
    ]