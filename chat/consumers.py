"""
Consumers are the equivalent of Django views for asynchronous applications.
They handle WebSockets in a very similar way to how traditional django views handle
HTTP requests.

Consumers are ASGI applications that can handle messages, notifications and are built
for long-running communication.

URLs are mapped to consumers through routing classes that allow us to combine and
stack consumers."""

import json

from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, code):
        pass

    def receive(self, text_data):
        data_dict = json.loads(text_data)
        message = data_dict["message"]

        # send message to websocket
        self.send(text_data=json.dumps({"message": message}))
