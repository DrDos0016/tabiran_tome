# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import urllib
import json
from sys import exit
from datetime import datetime, timedelta

class DeviantArt(object):
    def __init__(self, client_id, client_secret, mature_content=True):
        self.token = None
        self.token_expiration = 0
        self.token_type = None
        self.mature_content = mature_content
        self.client_id = client_id
        self.client_secret = client_secret
    
    def get_full_content(self, deviation_id):
        return self.send_request("deviation/content", deviationid=deviation_id)

    def get_gallery_content(self, folder_id, username="", mode="newest", offset=0, limit=10):
        # mode may be newest/popular. limit may be up to 24.
        return self.send_request("gallery/"+folder_id, username=username, mode=mode, offset=offset, limit=limit)
        
    def get_gallery_folders(self, username="", calculate_size=1, ext_preload=0, offset=0, limit=10):
        return self.send_request("gallery/folders", username=username, calculate_size=calculate_size, ext_preload=ext_preload, offset=offset, limit=limit)
        
    def get_token(self):
        url = "https://www.deviantart.com/oauth2/token?grant_type=client_credentials&client_id="+self.client_id+"&client_secret="+self.client_secret
        response = urllib.urlopen(url)
        data = json.load(response)
        if not data.get("status") == "success":
            print "Unable to get auth token! Exiting."
            exit()
            
        self.token = data["access_token"]
        self.token_expiration = datetime.now() + timedelta(seconds=data["expires_in"])
        self.token_type = data["token_type"]
        
    def get_user_journals(self, username, featured=0, offset=0, limit=10):
        return self.send_request("browse/user/journals", username=username, featured=featured, offset=offset, limit=limit)
        
    def send_request(self, operation, **kwargs):
        if not self.token:
            print "No token has been defined."
            return False
        url = "https://www.deviantart.com/api/v1/oauth2/"+operation
        url += "?access_token="+self.token
        for k,v in kwargs.iteritems():
            if v != "":
                url += "&"+str(k)+"="+str(v)
        #print "\nREQUEST:", url
        
        response = urllib.urlopen(url)
        data = json.load(response)
        return data
        
    def set_token(self, token, token_type="client_credentials", expires_on=0):
        self.token = token
        self.token_type = token_type
        self.token_expiration= expires_on
