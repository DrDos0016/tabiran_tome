#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def rank(guild, value):
    if guild == "Keepers":
        if value <= 0:
            return "Unaffiliated"
        elif value < 7:
            return "Initiate"
        elif value < 15:
            return "Preserver"
        elif value < 24:
            return "Warden"
        else:
            return "Guardian"
    elif guild == "Trackers":
        if value <= 0:
            return "Unaffiliated"
        elif value < 7:
            return "Initiate"
        elif value < 15:
            return "Scout"
        elif value < 24:
            return "Explorer"
        else:
            return "Adventurer"
    elif guild == "Scholars":
        if value <= 0:
            return "Unaffiliated"
        elif value < 7:
            return "Initiate"
        elif value < 15:
            return "Protégé"
        elif value < 24:
            return "Lector"
        else:
            return "Professor"
    elif guild == "Artisans":
        if value <= 0:
            return "Unaffiliated"
        elif value < 7:
            return "Initiate"
        elif value < 15:
            return "Apprentince"
        elif value < 24:
            return "Adept"
        else:
            return "Virtuoso"
    return "ERROR"
    
@register.simple_tag
def rank_images(guild, value):
    ranks = {"Keepers":["Preserver", "Warden", "Guardian"], "Trackers":["Scout", "Explorer", "Adventurer"], "Scholars":["Protégé", "Lector", "Professor"], "Artisans":["Apprentince", "Adept", "Virtuoso"]}
    
    if value < 7:
        level = 0
    elif value < 15:
        level = 1
    elif value < 24:
        level = 2
    else:
        level = 3
    
    if level == 0:
        output = '<img name="'+guild[0].lower()+'-1" src="/assets/images/badges/'+guild.lower()+'-1.png" title='+ranks[guild][0]+' class="darkened"><img name="'+guild[0].lower()+'-2" src="/assets/images/badges/'+guild.lower()+'-2.png" title='+ranks[guild][1]+' class="darkened"><img name="'+guild[0].lower()+'-3" src="/assets/images/badges/'+guild.lower()+'-3.png" title='+ranks[guild][2]+' class="darkened">'
    elif level == 1:
        output = '<img name="'+guild[0].lower()+'-1" src="/assets/images/badges/'+guild.lower()+'-1.png" title='+ranks[guild][0]+'><img name="'+guild[0].lower()+'-2" src="/assets/images/badges/'+guild.lower()+'-2.png" title='+ranks[guild][1]+' class="darkened"><img name="'+guild[0].lower()+'-3" src="/assets/images/badges/'+guild.lower()+'-3.png" title='+ranks[guild][2]+' class="darkened">'
    elif level == 2:
        output = '<img name="'+guild[0].lower()+'-1" src="/assets/images/badges/'+guild.lower()+'-1.png" title='+ranks[guild][0]+'><img name="'+guild[0].lower()+'-2" src="/assets/images/badges/'+guild.lower()+'-2.png" title='+ranks[guild][1]+'><img name="'+guild[0].lower()+'-3" src="/assets/images/badges/'+guild.lower()+'-3.png" title='+ranks[guild][2]+' class="darkened">'
    elif level == 3:
        output = '<img name="'+guild[0].lower()+'-1" src="/assets/images/badges/'+guild.lower()+'-1.png" title='+ranks[guild][0]+'><img name="'+guild[0].lower()+'-2" src="/assets/images/badges/'+guild.lower()+'-2.png" title='+ranks[guild][1]+'><img name="'+guild[0].lower()+'-3" src="/assets/images/badges/'+guild.lower()+'-3.png" title='+ranks[guild][2]+'>'
    output = mark_safe(output)
    return output