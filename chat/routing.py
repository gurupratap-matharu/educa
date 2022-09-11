"""
Channels provides routing classes that allows us to combine and stack consumers to
dispatch based on what the connection is.

We can think of them as the URL routing system of Django for asynchronous applications.
"""

from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/room/(?P<course_id>\d+)/$", consumers.ChatConsumer.as_asgi()),
]
