# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os, sys, django
sys.path.append("/var/projects/tales_of_tabira")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tabira.settings")
django.setup()
from tabira_web.models import *
from tabira_web.deviant_art import DeviantArt
from datetime import datetime
from tabira.private_settings import CLIENT_ID, CLIENT_SECRET

USERNAME = "talesoftabira"

def main():
    da = DeviantArt(CLIENT_ID, CLIENT_SECRET)
    da.get_token()
    Token.objects.update(value=da.token, updated=datetime.now())
    return True
    
if __name__ == "__main__":main()