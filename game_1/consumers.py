# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        response = json.loads(text_data)
        action = response.get("action", None)
        message = response.get("message", None)

        # можно добваить обработку if avtion == Move...
        if action == "CLOSE_SOCKET":
            await self.close()

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'action': action,
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        action = event.get("action", None)
        message = event.get("message", None)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'action': action
        }))


