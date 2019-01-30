"""
ASGI entrypoint file for default channel layer.

Points to the channel layer configured as "default" so you can point
ASGI applications at "databinding.asgi:channel_layer" as their channel layer.
"""

import os
import django
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OpsManage.settings")
django.setup()
application = get_default_application()
