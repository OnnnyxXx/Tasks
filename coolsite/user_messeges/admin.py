from django.contrib import admin
from user_messeges.models import Conversation, ConversationMessage

admin.site.register(Conversation)
admin.site.register(ConversationMessage)