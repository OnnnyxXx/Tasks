from .models import Profile, Comment
from django.forms import ModelForm, TextInput, Textarea, EmailInput, URLInput
from django import forms


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'city', 'profile_picture', 'telegram_url', "youtube_url",
                  "vk_url"]

        widgets = {
            "first_name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя'
            }),
            "last_name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваша Фамилия'
            }),
            "email": EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш email'
            }),
            "telegram_url": URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш Телеграмм (Не обязательно)'
            }),
            "youtube_url": URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш Ютуб Канал (Не обязательно)'
            }),
            "vk_url": URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш Вк (Не обязательно)'
            }),
            "city": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш город'
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProfileForm, self).__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields['email'].widget.attrs['value'] = user.email or "PUSTO"
            self.fields['first_name'].widget.attrs['value'] = user.first_name or "PUSTO"
            self.fields['last_name'].widget.attrs['value'] = user.last_name or "PUSTO"

            # Проверяем, что у пользователя есть профиль
            if hasattr(user, 'profile'):
                profile = user.profile
                self.fields['profile_picture'].widget.attrs['value'] = profile.profile_picture


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'stars']
        widgets = {
            "content": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Отзыв'
            }),
            "stars": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Звезды',

            })
        }
