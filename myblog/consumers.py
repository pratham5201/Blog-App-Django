# myblog/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

class PostConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.post_pk = self.scope['url_route']['kwargs']['post_pk']
        self.post_group_name = f'post_{self.post_pk}_group'

        # Join post group
        await self.channel_layer.group_add(
            self.post_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave post group
        await self.channel_layer.group_discard(
            self.post_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message': message}))

    async def post_update(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message': message}))

class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.post_pk = self.scope['url_route']['kwargs']['post_pk']
        self.post_group_name = f"post_{self.post_pk}_group"

        await self.channel_layer.group_add(
            self.post_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.post_group_name,
            self.channel_name
        )

    async def comment_update(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
