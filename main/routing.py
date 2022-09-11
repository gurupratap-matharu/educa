"""
Channels expects us to define a single root application that will be executed for
all requests.

We can define the root application by adding the ASGI_APPLICATION
setting to our project which is similar to the ROOT_URLCONF settings that points to
the base URL patterns of the project.

We can place this root application anywhere but its a convention to place it in
`routing.py` which is what this module is about.

Below the ProtocolTypeRouter automatically maps HTTP requests to the standard Django
views if no specific http mapping is provided.

The AuthMiddlewareStack class provided by channels supports standard Django authentication
where the user details are stored in the session.
"""

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import chat.routing

application = ProtocolTypeRouter(
    {
        "websocket": AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns)),
    }
)
