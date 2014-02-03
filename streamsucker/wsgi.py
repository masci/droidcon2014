"""
WSGI config for streamsucker project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
VENV_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# activate virtualenv
activate_this = os.path.join(VENV_DIR, "bin", "activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "streamsucker.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
