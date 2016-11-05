# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os, sys, django
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
sys.path.append("/var/projects/tales_of_tabira")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tabira.settings")
django.setup()
from tabira_web.models import *
from tabira_web.deviant_art import DeviantArt
from datetime import datetime
from tabira.private_settings import CLIENT_ID, CLIENT_SECRET

USERNAME = "talesoftabira"
if "debug" in sys.argv:
    debug = True
else:
    debug = False

def main():
    token = Token.objects.get(pk=1)
    da = DeviantArt(CLIENT_ID, CLIENT_SECRET)
    da.set_token(token.value)
    
    # Discover any new galleries
    offset = 0
    while True:
        galleries = da.get_gallery_folders(USERNAME, offset=offset)
        results = galleries.get("results")
        if results:
            for result in results:
                print(result)
                g, created = Gallery.objects.get_or_create(folder_id=result["folderid"])
                if created:
                    g.parent    = result.get("parent", "")
                    g.name      = result["name"]
                    g.monitor   = 1
                    g.save()
        
        if not galleries.get("has_more"):
            break
        else:
            offset = galleries["next_offset"]
    
    
    # Discover new deviations in each monitored gallery
    galleries_qs = Gallery.objects.filter(monitor=True)
    for gallery in galleries_qs:
        print("Processing gallery:", gallery.name)
        folder_id = gallery.folder_id
        offset = 0
        running = True
        while running:
            results = da.get_gallery_content(folder_id, username=USERNAME, offset=offset)
            deviations = results.get("results")
            if results:
                for deviation in deviations:
                    d, created = Deviation.objects.get_or_create(deviation_id=deviation["deviationid"], gallery=gallery)
                    if created:
                        #print("    [ ] " + deviation["title"])
                        d.da_url = deviation["url"]
                        d.title = deviation["title"]
                        d.author_name = deviation["author"]["username"]
                        d.author_id = deviation["author"]["userid"]
                        d.timestamp = deviation["published_time"]
                        try:
                            d.full_clean()
                            d.save()
                        except ValidationError as e:
                            print(e.message_dict)
                    else:
                        #print("    [X] " + deviation["title"])
                        if "force" not in sys.argv:
                            running = False
            
            if results.get("has_more") and running:
                offset = results["next_offset"]
            else:
                break
    return True
if __name__ == "__main__":main()
