from django.db import models
from django.contrib.auth.models import User


class Articles(models.Model):
    title = models.CharField("Название Задания", max_length=35)
    anons = models.CharField("О задании", max_length=25)
    phope = models.CharField('Телефон для связи с вами', max_length=11)
    prise = models.CharField('Цена', max_length=15)
    full_text = models.TextField("Задания")
    data = models.DateTimeField(auto_now_add=True)
    user_name = models.CharField("User_name", max_length=15, )
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Внешний ключ к пользователю

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


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    telegram_url = models.URLField(blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    vk_url = models.URLField(blank=True, null=True)
    profile_picture = models.ImageField("Изображения", default="logo.jpg", null=True, blank=True,
                                        upload_to='media/profile_pictures')

    def __str__(self):
        return self.user.username
