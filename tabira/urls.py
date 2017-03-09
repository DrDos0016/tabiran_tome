# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


"""tabira URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
import tabira_web.views
import tabira_web.admin

urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', tabira_web.views.index),

    # Admin functions
    url(r'^admin$', tabira_web.admin.admin),
    url(r'^admin/delete-pokemon$', tabira_web.admin.delete_pokemon),
    url(r'^admin/delete-team$', tabira_web.admin.delete_team),
    url(r'^admin/manage-events$', tabira_web.admin.manage_events),
    url(r'^admin/manage-items$', tabira_web.admin.manage_items),
    url(r'^admin/powerless$', tabira_web.admin.powerless),
    url(r'^admin/remove-author$', tabira_web.admin.remove_author),
    url(r'^admin/verify-teams$', tabira_web.admin.verify_teams),

    # AJAX functions

    # Chapter functions
    url(r'^chapter$', tabira_web.views.chapter),
    url(r'^chapter/list/(?P<key>[a-z0-9]+)/(?P<slug>.*)$', tabira_web.views.browse, {"method":"chapter"}),

    # Misc functions
    url(r'^misc$', tabira_web.views.generic, {"title":"Misc", "template":"misc.html"}),
    url(r'^misc/pokemon-listing$', tabira_web.views.pokemon_listing),
    url(r'^stats/population$', tabira_web.views.population),
    url(r'^stats/reputation/(?P<filter>.*)$', tabira_web.views.reputation),
    url(r'^stats/reputation$', tabira_web.views.reputation),

    # Team functions
    url(r'^team$', tabira_web.views.browse, {"method":"team"}),
    url(r'^team/edit/(?P<team_id>[-0-9]+)/(.*)/(?P<section>[a-z]+)$', tabira_web.views.team_edit),
    url(r'^team/view/(?P<team_id>[-0-9]+)/(.*)$', tabira_web.views.team_view),

    # User functions
    url(r'^sign-in$', tabira_web.views.sign_in),
    url(r'^sign-out$', tabira_web.views.sign_out),

    # Debugging functions
    url(r'^error$', tabira_web.views.error),
    url(r'^error/(?P<test>.*)$', tabira_web.views.error),
    url(r'^test$', tabira_web.views.test),

    # Easter Eggs because I can't resist
    url(r'^egg/simon$', tabira_web.views.generic, {"title":"SIMON", "template":"egg_simon.html"}),
]
