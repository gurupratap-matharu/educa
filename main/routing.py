"""
Channels expects us to define a single root application that will be executed for
all requests.

We can define the root application by adding the ASGI_APPLICATION
setting to our project which is similar to the ROOT_URLCONF settings that points to
the base URL patterns of the project.

We can place this root application anywhere but its a convention to place it in
`routing.py` which is what this module is about.
"""

from channels.routing import ProtocolTypeRouter

application = ProtocolTypeRouter(
    {
        # empty for now
    }
)
