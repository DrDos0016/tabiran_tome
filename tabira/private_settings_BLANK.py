# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


import os

"""
This file contains additional settings to be used in settings.py, split by developer environment.

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!! It is important to not leave this uploaded anywhere it can be publicly accessed !!!
!!! as it contains the site's key as well as MySQL credentials                      !!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

if os.path.isfile("/var/projects/DEV"):
    ENV = "DEV"
    DEBUG = True
else:
    ENV = "PROD"
    DEBUG = False
    
# DeviantArt API - https://www.deviantart.com/developers/
CLIENT_ID       = ""
CLIENT_SECRET   = ""

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '',
        'NAME': '',
        'USER': '',
        'PASSWORD': ''
    }
}
