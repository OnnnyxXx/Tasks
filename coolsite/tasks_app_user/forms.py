from .models import Articles
from django.forms import ModelForm, TextInput, Textarea, EmailInput, URLInput

from django import forms


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





# class SignUpForm(UserCreationForm):
#   email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
#    class Meta:
#        model = User
#        fields = ('username', 'email', 'password1', 'password2')

