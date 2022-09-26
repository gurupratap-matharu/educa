"""
Consumers are the equivalent of Django views for asynchronous applications.
They handle WebSockets in a very similar way to how traditional django views handle
HTTP requests.

Consumers are ASGI applications that can handle messages, notifications and are built
for long-running communication.

URLs are mapped to consumers through routing classes that allow us to combine and
stack consumers."""

import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.id = self.scope["url_route"]["kwargs"]["course_id"]
        self.room_group_name = "chat_%s" % self.id

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # Accept connection
        await self.accept()

    async def disconnect(self, code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data_dict = json.loads(text_data)
        message = data_dict["message"]
        now = timezone.now()

        # send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "user": self.user.username,
                "datetime": now.isoformat(),
            },
        )

    async def chat_message(self, event):
        """
        Receive message from the room group.

        This method is named as chat_message() to match the `type` key that is sent to
        the channel group when a message is received from the WebSocket.

        This way when a message with type `chat_message` is sent to the group, all
        consumers subscribed to the group will receive the message and will execute the
        `chat_message()` method.

        And we basically send the event message received to the WebSocket.
        """

        await self.send(text_data=json.dumps(event))
