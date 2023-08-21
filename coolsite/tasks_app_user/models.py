import time
from django.db import models
from django.contrib.auth.models import User


class Articles(models.Model):
    title = models.CharField("Название Задания", max_length=35)
    anons = models.CharField("О задании", max_length=25)
    phope = models.CharField('Телефон для связи с вами', max_length=11)
    prise = models.CharField('Цена', max_length=15)
    full_text = models.TextField("Задания")
    data = models.DateTimeField(auto_now_add=True)
    user_name = models.CharField("User_name", max_length=15)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Задания"
        verbose_name_plural = "Задании"

    def get_absolute_url(self):
        return f'/tasks/{self.id}'