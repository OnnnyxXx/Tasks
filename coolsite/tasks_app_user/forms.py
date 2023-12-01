from .models import Articles, Profile, Comment, ConversationMessage
from django.forms import ModelForm, TextInput, Textarea, EmailInput, URLInput

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class ArticlesForm(ModelForm):
    class Meta:
        model = Articles
        fields = ['title', 'anons', 'phope', 'prise', 'full_text', 'user_name', 'category']

        widgets = {
            "title": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Задания'
            }),
            "anons": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Что нужно с собой взять?'
            }),
            "phope": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Телефон для связи с вами'
            }),
            "prise": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Цена',

            }),
            "full_text": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Все о задании'
            }),

            "user_name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш Логин',
                "readonly": 'readonly'
            }),
            "category": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Категория',

            }),

        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Получите пользователя из kwargs
        super(ArticlesForm, self).__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields['user_name'].widget.attrs['value'] = user.username


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


class ConversationMessageForm(forms.ModelForm):
    class Meta:
        model = ConversationMessage
        fields = ['content']
        widgets = {
            "content": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Сообщения'
            }),
        }


# class SignUpForm(UserCreationForm):
#   email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
#    class Meta:
#        model = User
#        fields = ('username', 'email', 'password1', 'password2')

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Ваш Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
