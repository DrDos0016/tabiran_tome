# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


from django.shortcuts import render
from .common import *
from .views import error

def admin(request):
    data = {"title":"Administration"}
    if not request.session.get("admin"):
        return redirect("/")
    return render(request, 'admin/admin.html', data)

def delete_pokemon(request):
    data = {"title":"Delete Pokémon"}
    if not request.session.get("admin"):
        return redirect("/")
        
    if request.GET.get("team"):
        data["pokemon"] = Pokemon.objects.filter(team_id=request.GET.get("team"))
        data["team"] = Team.objects.get(pk=request.GET.get("team"))
        
    if request.POST:
        list = request.POST.getlist("delete")
        Pokemon.objects.filter(id__in=list).delete()
        return redirect("/team/view/"+str(data["team"].id)+"/"+slugify(data["team"].name))
        
    return render(request, 'admin/delete_pokemon.html', data)
    
def delete_team(request):
    data = {"title":"Delete Team"}
    if not request.session.get("admin"):
        return redirect("/")
        
    if request.GET.get("team"):
        data["team"] = Team.objects.get(pk=request.GET.get("team"))
        
    if request.POST:
        Pokemon.objects.filter(team_id=request.POST.get("delete")).delete()
        Team.objects.filter(pk=request.POST.get("delete")).delete()
        return redirect("/admin")
        
    return render(request, 'admin/delete_team.html', data)
    
def manage_items(request):
    data = {"title":"Manage Items"}
    if not request.session.get("admin"):
        return redirect("/")
        
    if request.POST:
        if request.POST["id"] == "new":
            item = Item()
        else:
            item = Item.objects.get(pk=int(request.POST["id"]))
            
        item.name = request.POST["name"]
        item.active = int(request.POST.get("active", 0))
        item.url = request.POST.get("url", "")
        
        # DL the image
        url = request.POST["image"]
        if url[:4] == "http":
            ret = urllib.urlretrieve(url, os.path.join(ROOT, "assets", "images", "items", slugify(request.POST["name"].lower())+".png"))
            item.image = slugify(request.POST["name"].lower())+".png"
        else:
            item.image = request.POST["image"]
        
        try:
            item.full_clean()
            item.save()
            return redirect("/admin/manage-items?item="+str(item.id))
        except ValidationError as e:
            return error(request, errors=e.message_dict)
        
    data["items"] = Item.objects.all().order_by("name")
    
    if request.GET.get("item"):
        data["wip"] = Item.objects.get(pk=request.GET["item"])
    
    return render(request, 'admin/manage_items.html', data)
    
def manage_events(request):
    data = {"title":"Manage Events"}
    if not request.session.get("admin"):
        return redirect("/")
        
    if request.POST:
        if request.POST["id"] == "new":
            event = Event()
        else:
            event = Event.objects.get(pk=int(request.POST["id"]))
            
        event.key = request.POST["key"].lower()
        event.name = request.POST["name"]
        event.active = int(request.POST.get("active", 0))
        event.timestamp = int(request.POST.get("timestamp", 0))
        event.order = int(request.POST.get("order", 999))
        #event.folder_id = request.POST.get("folder")
        
        # DL the image
        url = request.POST["image"]
        if url[:4] == "http":
            ret = urllib.urlretrieve(url, os.path.join(ROOT, "assets", "images", "chapters", request.POST["key"].lower()+".png"))
            event.image = request.POST["key"].lower()+".png"
        else:
            event.image = request.POST["image"]
        
        try:
            event.full_clean()
            event.save()
            return redirect("/admin/manage-events?event="+str(event.id))
        except ValidationError as e:
            return error(request, errors=e.message_dict)
        
    data["events"] = Event.objects.all().order_by("-id")
    data["galleries"] = Gallery.objects.all().order_by("name")
    
    if request.GET.get("event"):
        data["wip"] = Event.objects.get(pk=request.GET["event"])
    
    return render_to_response('admin/manage_events.html', data, context_instance=RequestContext(request))
    
def powerless(request):
    request.session["admin"] = 0
    request.session["icon"] = "/assets/images/sprites/icons/129.png"
    return redirect("/")
    
def remove_author(request):
    data = {"title":"Remove Author"}
    if not request.session.get("admin"):
        return redirect("/")
        
    if request.GET.get("team"):
        data["team"] = Team.objects.get(pk=request.GET.get("team"))
        
    if request.POST:
        list = request.POST.getlist("delete")
        for author in list:
            data["team"].authors.remove(author)
        #Owner.objects.filter(id__in=list).delete()
        return redirect("/team/view/"+str(data["team"].id)+"/"+slugify(data["team"].name))
        
    return render(request, 'admin/remove_author.html', data)
    
def verify_teams(request):
    data = {"title":"Verify Teams"}
    if not request.session.get("admin"):
        return redirect("/")
        
    if request.POST:
        list = request.POST.getlist("verify")
        Team.objects.filter(id__in=list).update(verified=1)
    else:
        data["checked"] = int(request.GET.get("team", 0))
    
    data["teams"] = Team.objects.filter(verified=0).order_by("name")
    return render(request, 'admin/verify_teams.html', data)