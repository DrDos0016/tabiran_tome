#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import template
from django.utils.safestring import mark_safe
from tabira_web.common import TABIRA_VALID, NAME_TO_NUM

register = template.Library()

@register.simple_tag
def pokemon_select(selected=0, any=False):
    output = '<select name="species">\n'
    if selected == "":
        selected = 0

    if any:
        output += '<option value="0">- Any -</option>\n'

    pokemon_list = TABIRA_VALID
    pokemon_list.sort()
    for pokemon in pokemon_list:
        number = NAME_TO_NUM.get(pokemon)
        if number == int(selected):
            output += '<option value="'+str(number)+'" selected>'+pokemon+'</option>\n'
        else:
            output += '<option value="'+str(number)+'">'+pokemon+'</option>\n'
    output += '</select>\n'

    output = mark_safe(output)
    return output
