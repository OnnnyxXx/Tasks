from django.contrib import admin
from .models import Articles, Profile, Comment, Conversation, ConversationMessage

admin.site.register(Articles)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Conversation)
admin.site.register(ConversationMessage)



