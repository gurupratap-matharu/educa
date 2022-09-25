"""
ASGI config for main project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

import django
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
django.setup()

"""
Load the default ASGI application using channels instead of the standard Django ASGI
module. This is because we wish to use Daphne with protocol servers.

Read more here: https://channels.readthedocs.io/en/latest/deploying.html#run-protocol-servers.
"""

application = get_default_application()
