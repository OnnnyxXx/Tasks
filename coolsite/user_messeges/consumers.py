import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async

from user_messeges.models import Conversation, ConversationMessage


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        created_at = await self.save_message(message, self.room_id, self.scope["user"])

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user_info': await self.get_user_info(self.scope["user"]),
                'created_at': created_at,
                'room_id': self.room_id
            }
        )

    async def chat_message(self, event):
        message = event['message']
        user_info = event['user_info']
        created_at = event['created_at']
        room_id = event['room_id']

        await self.send(text_data=json.dumps({
            'room_id': room_id,
            'message': message,
            'user_info': user_info,
            'time': created_at,
        }))

    @database_sync_to_async
    def get_user_info(self, user):
        if hasattr(user, 'profile'):
            profile = user.profile
            first_name = profile.first_name if hasattr(profile, 'first_name') else ''
            last_name = profile.last_name if hasattr(profile, 'last_name') else ''
            profile_picture_url = profile.profile_picture.url if hasattr(profile,
                                                                         'profile_picture') and profile.profile_picture else ''
            return {
                # 'username': user.username,
                'first_name': first_name,
                # 'last_name': last_name,
                'profile_image_url': profile_picture_url
            }
        return {
            # 'username': user.username,
        }

    @database_sync_to_async
    def save_message(self, message, room_id, user):
        conversation = Conversation.objects.get(id=room_id)
        new_message = ConversationMessage.objects.create(
            conversation=conversation,
            content=message,
            created_by=user
        )
        return new_message.created_at.strftime("%Y-%m-%d %H:%M:%S")
