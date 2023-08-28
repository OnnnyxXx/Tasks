from .models import Articles, Profile
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class ArticlesForm(ModelForm):
    class Meta:
        model = Articles
        fields = ['title', 'anons', 'phope', 'prise', 'full_text', 'user_name']

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
                'placeholder': 'Цена'
            }),
            "full_text": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Все о задании'
            }),

            "user_name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш Логин'
            }),

        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'profile_picture']


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
