# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from common import *

def chapter(request):
    data = {"title":"Chapter Listing"}
    data["chapters"] = Event.objects.all().order_by("-order")
    return render_to_response('chapter.html', data, context_instance=RequestContext(request))

def error(request, errors={}):
    data = {"title":"Error!"}
    data["errors"] = []
    for key in errors.keys():
        data["errors"].append(key + ": " + str(errors[key]) + "\n")
        
    
    data["meta"]  = "TIMESTAMP : " + str(datetime.now()) + "\n"
    data["meta"] += "PATH      : " + request.get_full_path() + "\n"
    data["meta"] += "IP        : " + request.META["REMOTE_ADDR"] + "\n"
    data["meta"] += "USER AGENT: " + request.META["HTTP_USER_AGENT"] + "\n"
    data["meta"] += "GET       : " + str(request.GET.items()) + "\n"
    data["meta"] += "POST      : " + str(request.POST.items()) + "\n"
    if not request.session.get("logged_in"):
        data["meta"] += "USER      : GUEST" + "\n"
    else:
        data["meta"] += "USER      : " + request.session.get("username") + "\n"
        data["meta"] += "USER ID   : " + str(request.session.get("user_id")) + "\n"
        data["meta"] += "DA ID     : " + request.session.get("da_id") + "\n"
        data["meta"] += "BETA      : " + str(request.session.get("beta")) + "\n"
        data["meta"] += "ADMIN     : " + str(request.session.get("admin")) + "\n"
    return render_to_response('error.html', data, context_instance=RequestContext(request))

def generic(request, title="", template=""):
    data = {"title":title}
    return render_to_response(template, data, context_instance=RequestContext(request))

def index(request): # Index/Manage Teams
    data = {"title":"Table of Contents"}
    data["today"] = str(datetime.now())[:10]
    data["welcome"] = request.GET.get("welcome", False)
    # Create a new team
    if request.session.get("logged_in"):        
        if request.POST.get("name") and request.POST.get("joined"):
            team = Team(name=request.POST["name"], joined=request.POST["joined"], type=request.POST["type"], cameos=request.POST["cameos"])
            if request.session.get("admin"):
                team.verified = True
            try:
                team.full_clean()
                team.save()
                team.authors.add(request.session["user_id"])
                return redirect("/team/view/"+str(team.id)+"/"+slugify(team.name))
            except ValidationError as e:
                return error(request, errors=e.message_dict) 
                
        data["teams"] = Team.objects.filter(authors=request.session.get("user_id")).prefetch_related("authors", "teammates").order_by("name")
    else:
        data["welcome"] = True
    
    return render_to_response('index.html', data, context_instance=RequestContext(request))
    
def sign_in(request):
    data = {"title":"Sign In"}
    
    if ENV == "DEV":
        uri = "http://django.pi:8000/sign-in"
    else:
        uri = "http://tome.pokyfriends.com/sign-in"
        
    if not request.GET.get("code"):
        return redirect("https://www.deviantart.com/oauth2/authorize?response_type=code&client_id="+CLIENT_ID+"&redirect_uri="+uri)
    else:
        url = "https://www.deviantart.com/oauth2/token?client_id="+CLIENT_ID+"&client_secret="+CLIENT_SECRET+"&grant_type=authorization_code&code="+request.GET["code"]+"&redirect_uri="+uri
        
        if ENV == "DEV" and False:
            # Standard
            response = urllib2.urlopen(url)
            data = json.load(response)
            token = data["access_token"]
            response = urllib2.urlopen("https://www.deviantart.com/api/v1/oauth2/user/whoami?access_token="+token)
            data = json.load(response)
        else:
            if ENV == "DEV":
                print "Forcing external login system. (Yuk!)"
            # Ext script
            os.system("/usr/local/bin/python2.7.10 /var/projects/tales_of_tabira/tabira_web/login.py " + request.META.get("REMOTE_ADDR").replace(".", "") + " \"" + url + "\"")
            # Read file
            data = open("/var/projects/tales_of_tabira/assets/data/logins/"+request.META.get("REMOTE_ADDR").replace(".", "")+".json").read()
            data = json.loads(data)
            if data:
                os.remove("/var/projects/tales_of_tabira/assets/data/logins/"+request.META.get("REMOTE_ADDR").replace(".", "")+".json")
        
        request.session["logged_in"] = True
        request.session["username"] = data["username"]
        request.session["da_id"] = data["userid"]
        request.session["icon"] = data["usericon"]
        
        user, created = User.objects.get_or_create(da_id=data["userid"])
        user.username = data["username"]
        user.icon = data["usericon"]
        user.ip = request.META.get("REMOTE_ADDR")
        
        try:
            user.full_clean()
            user.save()
        except ValidationError as e:
            return error(request, errors=e.message_dict) 
        
        request.session["user_id"] = user.id
        request.session["beta"] = user.beta
        request.session["admin"] = user.admin
        return redirect("/")
        
    return redirect("/error")
    
def sign_out(request):
    request.session.flush()
    return redirect("/")
    
def browse(request, method, key=None, slug=None):
    if method == "team":
        data = {"title":"Team Listing", "base_url":"/team"}
    elif method == "chapter":
        data = {"title":"Submitted Chapters", "base_url":"/chapter/list/"+str(key)+"/"+str(slug)}
        possible_teams = Logbook.objects.filter(event__key=key).distinct().values_list("team_id", flat=True)
    
    tpp = 15 # Teams Per Page
    page = int(request.GET.get("page", 1))
    
    prev_params = request.GET.copy()
    next_params = request.GET.copy()
    
    prev_params["page"] = max(page - 1, 1)
    next_params["page"] = page + 1
    
    data["prev"] = prev_params.urlencode
    data["next"] = next_params.urlencode
    
    data["page"] = page
    data["method"] = method
    
    # Filter results
    if method == "team":
        data["teams"] = Team.objects.filter(verified=True).prefetch_related("teammates")
    elif method == "chapter":
        data["teams"] = Team.objects.filter(verified=True, id__in=possible_teams).prefetch_related("teammates")
    
    if request.GET.get("name"):
        data["teams"] = data["teams"].filter(name__icontains=request.GET["name"])
    if request.GET.get("author"):
        authors_teams = Owner.objects.filter(user__username__icontains=request.GET["author"]).values_list("team_id", flat=True)
        data["teams"] = data["teams"].filter(id__in=authors_teams)
    
    if request.GET.get("species") and request.GET["species"] != "0":
        if int(request.GET.get("active", 0)):
            if request.GET.get("match") == "species": # Species/Line
                data["teams"] = data["teams"].filter(teammates__species=request.GET["species"], teammates__status="Active")
            elif request.GET.get("match") == "evolution":
                data["teams"] = data["teams"].filter(teammates__species_line=PKMN_TO_CHAIN.get(int(request.GET["species"], 0)), teammates__status="Active")
        else:
            if request.GET.get("match") == "species": # Species/Line
                data["teams"] = data["teams"].filter(teammates__species=request.GET["species"])
            elif request.GET.get("match") == "evolution":
                data["teams"] = data["teams"].filter(teammates__species_line=PKMN_TO_CHAIN.get(int(request.GET["species"], 0)))
    
    if request.GET.get("teammate"):
        data["teams"] = data["teams"].filter(teammates__name__icontains=request.GET["teammate"])
    if request.GET.get("cameos"):
        if request.GET["cameos"] == "Yes":
            data["teams"] = data["teams"].filter(cameos="Yes")
        if request.GET["cameos"] == "No":
            data["teams"] = data["teams"].filter(cameos="No")
        if request.GET["cameos"] == "Ask":
            data["teams"] = data["teams"].filter(cameos="Ask")
        if request.GET["cameos"] == "Non-Speaking":
            data["teams"] = data["teams"].filter(cameos="Non-Speaking")
    if request.GET.get("tumblr") and request.GET["tumblr"] != "Any":
        if request.GET["tumblr"] == "Yes":
            data["teams"] = data["teams"].exclude(tumblr="")
        elif request.GET["tumblr"] == "No":
            data["teams"] = data["teams"].filter(tumblr="")
    if request.GET.get("type") and request.GET["type"] != "Any":
        data["teams"] = data["teams"].filter(type=request.GET["type"])
    
    sort_methods = {"latest":"-id", "name":"name", "random":"?"}
    sort = sort_methods.get(request.GET.get("sort"), "-id")
    
    data["teams"] = data["teams"].order_by(sort)[(page-1)*tpp:(page-1)*tpp+tpp]
    data["query"] = data["teams"].query
    if ENV == "DEV":
        print data["query"]
        
    if method == "chapter":
        for team in data["teams"]:
            team.logbook = team.logbooks.filter(event__key=key)
        
    # Append logbook info
    return render_to_response("browse.html", data, context_instance=RequestContext(request))
    
def team_edit(request, team_id, section):
    data = {"title":"Edit Team - " + section.title()}
    data["section"] = section
    team = get_object_or_404(Team, pk=team_id)
    
    if section == "chapters":
        data["submissions"] = Logbook.objects.filter(team_id=team_id) # Events you already submitted
        
        if not data["submissions"]: # Force the first logbook to be your app
            data["events"] = Event.objects.filter(pk=APP_EVENT_ID)
            data["newbie"] = True
        else:
            data["events"] = Event.objects.all().order_by("-id")
    
        for event in data["events"]:
            event.current_submitted = 0
            for submission in data["submissions"]:
                if submission.event_id == event.id:
                    event.current_submitted += 1
    
        data["author_ids"] = []
        for author in team.authors.all():
            data["author_ids"].append(author.da_id)
            
        data["deviations"] = Deviation.objects.filter(author_id__in=data["author_ids"])
        
    if section == "inventory":
        data["items"] = Item.objects.all().order_by("name")
    
    if request.POST:
        if section == "team":
            changes = ""
            if team.name != request.POST.get("name"):
                changes += "Edited " + team.name + " to " + request.POST.get("name") + ". "
                team.name = request.POST.get("name")
            if team.joined != request.POST.get("joined"):
                team.joined = request.POST.get("joined")
                changes += "Edited join date of " + team.joined + " to " + request.POST.get("joined") + "."
            try:
                team.full_clean()
                team.save()
                feed_post("TEAM", changes, request.session.get("user_id"), team.id)
                return redirect("/team/view/"+str(team.id)+"/"+slugify(team.name.lower()))
            except ValidationError as e:
                return error(request, errors=e.message_dict)
                
        if section == "teammates":
            team = Team.objects.filter(pk=team_id).prefetch_related("teammates")[0]
            pokemon = team.teammates.all()
            
            if len(pokemon) != len(request.POST.getlist("id")):
                return redirect("/error", errors=["Array length mismatch!"])
            
            # Update existing Pokemon
            ids = request.POST.getlist("id")
            names = request.POST.getlist("name")
            species = request.POST.getlist("species")
            genders = request.POST.getlist("gender")
            statuses = request.POST.getlist("status")
            shinies = request.POST.getlist("shiny")
            
            # Limit of 4 active Pokémon
            active_count = 0
            for x in xrange(0, len(pokemon)):
                if statuses[x].title() == "Active":
                    active_count += 1
            if active_count > 4:
                return error(request, errors={"error":"You may have no more than four active teammates at a time."})
            
            for x in xrange(0, len(pokemon)):
                changes = ""
                poke = pokemon[x]
                if poke.id != int(ids[x]):
                    return redirect("/error", errors=["POST id/Teammate id mismatch!"])
                
                if poke.status != statuses[x].title():
                    poke.status = statuses[x].title()
                    changes += "Updated status for " + names[x] + " to be " + statuses[x].title() +". "
                
                if (poke.name != names[x]) or (poke.species != int(species[x])) or (poke.gender != genders[x]) or (int(poke.shiny) != int(shinies[x])):
                    changes += "Updated " + poke.name + " the " + poke.gender + " " + (int(poke.shiny)*"shiny ") + poke.species_name() + " to "
                    poke.name = names[x]
                    poke.species = int(species[x])
                    poke.update_species_line()
                    poke.gender = genders[x]
                    poke.shiny = shinies[x]
                    changes += poke.name + " the " + (int(poke.shiny)*"shiny ") + poke.gender + " " + poke.species_name() + ". "
                
                try:
                    poke.full_clean()
                    poke.save()
                    if changes:
                        feed_post("POKEMON", changes, request.session.get("user_id"), team.id)
                except ValidationError as e:
                    return error(request, errors=e.message_dict)
            
            # Add new Pokemon if necessary
            if names[-1] != "":
                poke = Pokemon(name=names[-1], species=species[-1], gender=genders[-1], status=statuses[-1].title(), shiny=shinies[-1])
                poke.species_line = PKMN_TO_CHAIN.get(int(species[-1]), -1)
                try:
                    poke.full_clean()
                    poke.save()
                    changes += "Added new teammate " + poke.name + " the " + poke.gender + " " + (int(poke.shiny)*"shiny ") + poke.species_name()
                    feed_post("POKEMON", changes, request.session.get("user_id"), team.id)
                    team.teammates.add(poke)
                except ValidationError as e:
                    return error(request, errors=e.message_dict)
                
            
            reason = request.POST.get("why") if request.POST.get("why") else "None given. "
            feed_post("POKEMON", ("Edited Pokémon. Reasoning: " + reason), request.session.get("user_id"), team.id)
            # Redirect
            return redirect("/team/view/"+str(team_id)+"/"+slugify(team.name.lower()))
                
        if section == "reputation":
            (old_k, old_t, old_s, old_a) = (team.rep_keepers, team.rep_trackers, team.rep_scholars, team.rep_artisans)
            team.rep_keepers    = request.POST.get("rep-k", 0)
            team.rep_trackers   = request.POST.get("rep-t", 0)
            team.rep_scholars   = request.POST.get("rep-s", 0)
            team.rep_artisans   = request.POST.get("rep-a", 0)
            try:
                team.full_clean()
                team.save()
                changes = "Adjusted reputation from " + str(old_k)+"K/" + str(old_t) +"T/" + str(old_s) +"S/" + str(old_a) +"A, to "
                changes += str(team.rep_keepers)+"K/" + str(team.rep_trackers) +"T/" + str(team.rep_scholars) +"S/" + str(team.rep_artisans) +"A. "
                changes += "Reasoning: " + request.POST.get("why", "None given.")
                feed_post("REPUTATION", changes, request.session.get("user_id"), team.id)
                return redirect("/team/view/"+str(team.id)+"/"+slugify(team.name.lower()))
            except ValidationError as e:
                return error(request, errors=e.message_dict)
                
        if section == "favor":
            old_earned = team.favor_earned
            team.favor_earned   = request.POST.get("earned", 0)
            old_spent = team.favor_spent
            team.favor_spent   = request.POST.get("spent", 0)
            
            try:
                team.full_clean()
                team.save()
                changes = "Adjusted favor from " + str(old_earned) + " earned / " + str(old_spent) + " spent, to " + str(team.favor_earned) + " earned / " + str(team.favor_spent) + " spent. "
                changes += "Reasoning: " + request.POST.get("why", "None given.")
                feed_post("FAVOR", changes, request.session.get("user_id"), team.id)
                return redirect("/team/view/"+str(team.id)+"/"+slugify(team.name.lower()))
            except ValidationError as e:
                return error(request, errors=e.message_dict)
       
        if section == "chapters":
            if "Save" in request.POST.get("method", ""):
                # New or Existing
                if request.POST.get("submission") == "NEW":
                    logbook = Logbook(event_id = request.POST.get("event_id"))
                    changes = "Added new chapter for event #" + str(logbook.event_id)
                else:
                    logbook = Logbook.objects.get(pk=request.POST.get("submission"))
                    changes = "Edited chapter for event #" + str(logbook.event_id)
                    
                # TODO: Logbook ordering
                #logbook.order = 
                logbook.custom_name = request.POST.get("custom_name", "")
                logbook.event_id        = request.POST.get("event_id")
                logbook.deviation_id    = request.POST.get("deviation_id")
                try:
                    logbook.full_clean()
                    logbook.save()
                    team.logbooks.add(logbook)
                    feed_post("CHAPTERS", changes, request.session.get("user_id"), team.id)
                    return redirect("/team/view/"+str(team.id)+"/"+slugify(team.name.lower()))
                except ValidationError as e:
                    return error(request, errors=e.message_dict)
            else: # Delete
                try:
                    logbook = Logbook.objects.get(pk=request.POST.get("submission"))
                    team.logbooks.remove(logbook)
                    logbook.delete()
                    return redirect("/team/view/"+str(team.id)+"/"+slugify(team.name.lower()))
                except ValidationError as e:
                    return error(request, errors=e.message_dict)
       
        if section == "inventory":
            if request.POST.get("action") == "Add":
                inventory = Inventory(item_id=request.POST.get("item"), team_id=team.id)
                inventory.save()
                feed_post("INVENTORY", "Added " + inventory.item.name + " to the team's inventory. Reasoning: " + request.POST.get("why", "None given.") , request.session.get("user_id"), team.id)
                return redirect("/team/view/"+str(team.id)+"/"+slugify(team.name.lower()))
            elif request.POST.get("action") == "Remove":
                matches = Inventory.objects.filter(item_id=request.POST.get("item"), team_id=team.id)
                if matches:
                    feed_post("INVENTORY", "Removed " + matches[0].item.name + " from the team's inventory. Reasoning: " + request.POST.get("why", "None given.") , request.session.get("user_id"), team.id)
                    matches[0].delete()
                return redirect("/team/view/"+str(team.id)+"/"+slugify(team.name.lower()))
       
        if section == "meta":
            changes = ""
            if team.type != request.POST.get("type"):
                changes += "Adjusted team type from " + team.type + " to " + request.POST.get("type") + ". "
                team.type = request.POST.get("type")
            if team.cameos != request.POST.get("cameos"):
                changes += "Adjusted cameo preferences from " + team.cameos + " to " + request.POST.get("cameos") + ". "
                team.cameos = request.POST.get("cameos")
            if team.tumblr != request.POST.get("tumble"):
                changes += "Adjusted team tumblr from " + team.tumblr + " to " + request.POST.get("tumblr") + ". "
                team.tumblr = request.POST.get("tumblr")
            
            if request.POST.get("author"):
                # Check the author exists
                lookup = User.objects.filter(username=request.POST.get("author"))
                if lookup:
                    lookup = lookup[0]
                    user_id = lookup.id
                    team.authors.add(user_id)
                    changes += "Added " + lookup.username + " as a new co-author. "
                else:
                    return error(request, errors={"error":"The author specified was not found!"})
            
            try:
                team.full_clean()
                team.save()
                feed_post("META", changes, request.session.get("user_id"), team.id)
                return redirect("/team/view/"+str(team.id)+"/"+slugify(team.name.lower()))
            except ValidationError as e:
                return error(request, errors=e.message_dict)
            
    
    data["team"] = team
    return render_to_response("team_edit.html", data, context_instance=RequestContext(request))
    
def team_view(request, team_id=None):
    data = {}
    data["reserved_ids"] = RESERVED_IDS
    data["team"] = get_object_or_404(Team, pk=team_id)
    for author in data["team"].authors.all():
        if request.session.get("user_id") == author.id:
            data["yours"] = True
    
    data["title"] = "["+str(data["team"].id)+"] " + data["team"].name
    data["pokemon"] = Pokemon.objects.filter(team_id=team_id)
    data["logbooks"] = Logbook.objects.filter(team_id=team_id)
    for logbook in data["logbooks"]:
        if logbook.event.id == APP_EVENT_ID:
            data["app"] = logbook
        if logbook.event.id == INVENTORY_EVENT_ID:
            data["inv"] = logbook
            
        if data.get("app") and data.get("inv"):
            break
    data["inventory"] = Inventory.objects.filter(team_id=team_id).order_by("item__name")
    if PUBLIC_FEEDS or (request.session.get("admin") or data["yours"]):
        fpp = 10
        page = int(request.GET.get("page", 1))
        data["prev"] = max(page - 1, 1)
        data["next"] = page + 1
        data["feed"] = Feed.objects.filter(team_id=team_id).order_by("-id")[(page-1)*fpp:(page-1)*fpp+fpp]
        data["has_feed"] = True
    return render_to_response("team_view.html", data, context_instance=RequestContext(request))
    
def test(request):
    from django import VERSION
    from sys import version
    output = "Django: " + str(VERSION) + "<br>"
    output += "Python: " + str(version) + "<br>"
    return HttpResponse(output)