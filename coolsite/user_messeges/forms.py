from django import forms
from django.forms import Textarea

from user_messeges.models import ConversationMessage


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
