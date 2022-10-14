"""
WSGI config for epl343 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/home/EPL343_PROJECT/epl343.winter22.teamX')
sys.path.append('/home/EPL343_PROJECT/epl343.winter22.teamX/epl343')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'epl343.settings')

application = get_wsgi_application()
