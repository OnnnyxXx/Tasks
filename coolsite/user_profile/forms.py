from .city import cities_of_russia
from .models import Profile, Comment
from django.forms import ModelForm, TextInput, Textarea, EmailInput, URLInput
from django import forms


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'city', 'profile_picture', 'telegram_url', 'youtube_url',
                  'vk_url']
        widgets = {
            "first_name": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            "last_name": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваша Фамилия'}),
            "email": forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ваш email'}),
            "telegram_url": forms.URLInput(
                attrs={'class': 'form-control', 'placeholder': 'Ваш Телеграмм (Не обязательно)'}),
            "youtube_url": forms.URLInput(
                attrs={'class': 'form-control', 'placeholder': 'Ваш Ютуб Канал (Не обязательно)'}),
            "vk_url": forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Ваш Вк (Не обязательно)'}),
            "city": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш город'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProfileForm, self).__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields['email'].widget.attrs['value'] = user.email or "Ваш email"
            self.fields['first_name'].widget.attrs['value'] = user.first_name or "Ваше Имя"
            self.fields['last_name'].widget.attrs['value'] = user.last_name or "Ваша Фамилия"
            self.fields['city'].widget.attrs['value'] = user.profile.city or "Ваш Город"

            if hasattr(user, 'profile'):
                profile = user.profile
                self.fields['profile_picture'].widget.attrs['value'] = profile.profile_picture

    def clean_city(self):
        city = self.cleaned_data.get('city')
        if city not in cities_of_russia:
            raise forms.ValidationError("Город не найден. Либо напишите его с большой буквы")
        return city


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
