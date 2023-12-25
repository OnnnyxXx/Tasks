from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    def __str__(self):
        return self.name


class Articles(models.Model):
    title = models.CharField("Название Задания", max_length=35)
    anons = models.CharField("О задании", max_length=25)
    phope = models.CharField('Телефон для связи с вами', max_length=11)
    prise = models.CharField('Цена', max_length=15)
    full_text = models.TextField("Задания")
    data = models.DateTimeField(auto_now_add=True)
    user_name = models.CharField("User_name", max_length=15, )
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Внешний ключ к пользователю
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Задания"
        verbose_name_plural = "Задании"

    def save(self, *args, **kwargs):
        # Автоматически заполняем поле author при сохранении статьи
        if not self.author:
            self.author = User.objects.get(username=self.user_name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f'/tasks/{self.id}'

