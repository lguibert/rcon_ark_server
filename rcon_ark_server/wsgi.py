"""
WSGI config for rcon_ark_server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys

#sys.path.append('/var/python-www/rcon_ark_server')
sys.path.append('E:/wamp/www/rcon_ark_server')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rcon_ark_server.settings")

application = get_wsgi_application()
