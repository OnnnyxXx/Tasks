from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
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
    profile_picture = models.ImageField("Изображения", default="profile_pictures/default_profile_picture.jpg", null=True,
                                        blank=True, upload_to='media/profile_pictures')
    city = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    stars = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])  # Добавляем поле для звездочек
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Author: {self.author.username}, Profile: {self.profile.user.username}, Stars: {self.stars}, Content: {self.content}"


class Conversation(models.Model):
    item = models.ForeignKey(Articles, related_name='conversations', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-modified_at',)


class ConversationMessage(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_messages', on_delete=models.CASCADE)