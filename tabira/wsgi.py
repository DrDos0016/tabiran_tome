"""
WSGI config for tabira project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os, sys, site

site.addsitedir('/var/projects/tales_of_tabira/virt/local/lib/python2.7/site-packages')
sys.path.append("/var/projects")
sys.path.append("/var/projects/tales_of_tabira")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tabira.settings")

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tabira.settings")

application = get_wsgi_application()
