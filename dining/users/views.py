from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from users.models import NetID
from users.models import Item
import sys, time
import json
import string

#david experiment
from django.template.loader import get_template
from django.template import Context # for inserting data from our view in correct place
#import sqlite3 as lite
from django.views.generic.base import TemplateView # a view that knows how to display a template
from users.models import NetID 
from django.shortcuts import render_to_response
#from django.config import settings
import Levenshtein
import MySQLdb

def load_index_context(request):
    file = open('/home/ubuntu/TigerBites/dining/today.json')
    today = json.load(file)
    file.close()
    menu = []
    for dic in today:
        menu.append((dic['dhall'], dic['meal'], dic['menus']))
    template = loader.get_template('users/index.html')
    context = RequestContext(request, {'menu' : menu})
    return context


def index(request):
    #get today.json from parent directory
    file = open('/home/ubuntu/TigerBites/dining/today.json')
    today = json.load(file)
    file.close()
    menu = []
    bf = False;
    lc = False;
    dn = False;
    matched = False
    for dic in today: 
        menu.append((dic['dhall'], dic['meal'], dic['menus']))
        if dic['meal'] == 'BREAKFAST':
            bf = True
        elif dic['meal'] == 'LUNCH':
            lc = True
        elif dic['meal'] == 'DINNER':
            dn = True
    template = loader.get_template('users/index.html')
    authenticated = request.user.is_authenticated()
    date = time.strftime("%A, %b %d")
    faves = []

    if request.method == 'POST':
        food = request.POST.get('addItem')
        removefood = request.POST.get('removeItem')
        if request.user.is_authenticated():
            idy = request.user.get_username()
            item = Item.objects.filter(name = food)
            item2 = Item.objects.filter(name = removefood)
            person, isNew = NetID.objects.get_or_create(netid = idy)

            if len(item) == 0: 
                if len(item2) == 0:                                                                    
                #this shouldn't happen                                                            
                    return HttpResponse("oh noes, this item should be in the db and it isn't! Please contact princetontigerbites@gmail.com")        
            if len(item) == 1:                                                                    
                for thing in item:                                                               
                    person.favorites.add(thing)
            if len(item2) == 1:
                for thing in item2:
                    person.favorites.remove(thing)
            if len(item) > 1:                                                                     
                #this also shouldn't happen                                                            
                return HttpResponse("oh noes, this item seems to be in the db more than once! Please contact princetontigerbites@gmail.com")    
            person.save()
            template = loader.get_template('users/index.html')
           
            faves = person.favorites.all()
            faves2 = []
            for i in faves:
               faves2.append((i.name.encode('utf-8')))
               
            for dhall, meal, item, in menu:
                for i in item:
                    if i["name"] in faves2:
                        matched = True
                        break

            context = RequestContext(request, {'menu' : menu, 'matched':matched, 'loggedin' : authenticated, 'bf': bf, 'lc': lc, 'dn' : dn, 'favorites' : faves2, 'added' : food, 'removed' : removefood, 'date': date})
            return HttpResponse(template.render(context))
        else:
            return HttpResponseRedirect('/accounts/login/')

    if authenticated:
        matched = False
        idy = request.user.get_username()
        person, isNew = NetID.objects.get_or_create(netid = idy)
        if isNew:
            faves2 = ['0']
        else:
            faves = person.favorites.all()
            #faves = [str(person.favorites.count())]
            faves2 = []
        for i in faves:
            if not isinstance(i, str):
                b = i
                nameonly = b.name
                faves2.append((nameonly.encode('utf-8')))
        for dhall, meal, item, in menu:
            for i in item:
                if i["name"] in faves2:
                    matched= True
                    break

        context = RequestContext(request, {'menu' : menu, 'matched': matched,'loggedin' : authenticated, 'bf': bf, 'lc': lc, 'dn' : dn, 'favorites' : faves2, 'date': date})
    else:
        context = RequestContext(request, {'menu' : menu, 'loggedin' : authenticated, 'bf': bf, 'lc': lc, 'dn' : dn,'date':date})
    return HttpResponse(template.render(context))






def favorites(request):
    if request.method == 'POST':
        food = request.POST.get('removeItem')
        idy = request.user.get_username()
        item = Item.objects.filter(name = food)
        person, isNew = NetID.objects.get_or_create(netid = idy)
        if len(item) == 0:
            #this shouldn't happen
            return HttpResponse("oh noes, this item should be in the db and it isn't!")
        if len(item) == 1:
            for thing in item:
                person.favorites.remove(thing)
        if len(item) > 1:
            #this also shouldn't happen                                                                                   
            return HttpResponse("oh noes, this item seems to be in the db more than once!")
        person.save()

    if request.user.is_authenticated():
        idy = request.user.get_username()
        person = NetID.objects.filter(netid = idy)
        faves = []
        if len(person) == 0:
            faves = ['You don\'t have any favorites! Go find some!']          
        if len(person) == 1:
            person = list(person)
            faves = person[0].favorites.all()
        if len(person) > 1:
            faves = [("something went wrong, cause you're in the database" + str(len(person)) + "times")]
        template = loader.get_template('users/favorites.html')
        faves2 = []
        for i in faves:
            faves2.append((i.name.encode('utf-8')))
        context = RequestContext(request, {'netid': request.user.get_username(), 'favorites':faves2})
        return HttpResponse(template.render(context))
    else:
        return HttpResponseRedirect('/accounts/login/')




def search(request):

    if 's1' in request.GET:

        query = request.GET['s1']
        template = loader.get_template('search.html')
        authenticated = request.user.is_authenticated()
        faves2 = []
        if authenticated:
            idy = request.user.get_username()
            person = NetID.objects.filter(netid = idy)
            faves = []
            if len(person) == 1:
                person = list(person)
                faves = person[0].favorites.all()

            for i in faves:
                faves2.append((i.name.encode('utf-8')))

        con = MySQLdb.connect(user='tigerbites', db='db_mysql',passwd='princetoncos333', host='localhost') 
        result = []
        with con:
            cur = con.cursor()
            
            cur.execute("SELECT * FROM users_item")
            for food in cur.fetchall():
                similarity = Levenshtein.ratio(food[6], query.encode('utf-8'))
                if (len(food[6]) > len(query)):
                    ratio = float(len(query))/float(len(food[6]))
                else:
                    ratio = float(len(food[6]))/float(len(query))

                if query.encode('utf-8').lower() in food[6].lower() or food[6].lower() in query.encode('utf-8').lower() or similarity > 0.7:
                    encoded_food = unicode(food[6], errors= 'ignore')#'replace') # this is where the unicode problem was occuring
                    if 'Sauted' in encoded_food:
                        encoded_food = encoded_food[0:4] + u'\u00E9' + encoded_food[4:]
                    result.append(encoded_food)
        result.sort()
        context = RequestContext(request, {'query': query, 'loggedin' : authenticated, 'result': result, 'favorites' : faves2})
        return HttpResponse(template.render(context))
    elif request.method == 'POST':
        template = loader.get_template('search.html')
        authenticated = request.user.is_authenticated()
        food = request.POST.get('addItem')
        removefood = request.POST.get('removeItem')
        query = request.POST.get('searched')
        result = request.POST.getlist('result')
        if request.user.is_authenticated():
            idy = request.user.get_username()
            item = Item.objects.filter(name = food)
            item2 = Item.objects.filter(name = removefood)
            person, isNew = NetID.objects.get_or_create(netid = idy)

            if len(item) == 0: 
                if len(item2) == 0:                                                                    
                #this shouldn't happen                                                            
                    return HttpResponse("oh noes, " + food + "should be in the db and it isn't! we'd appreciate an email at tigerbites@gmail.com")        
            if len(item) == 1:                                                                    
                for thing in item:                                                               
                    person.favorites.add(thing)
            if len(item2) == 1:
                for thing in item2:
                    person.favorites.remove(thing)
            if len(item) > 1:                                                                     
                #this also shouldn't happen                                                            
                return HttpResponse("oh noes, this item seems to be in the db more than once! we'd appreciate an email at tigerbites@gmail.com")    
            person.save()
                   
            faves = person.favorites.all()
            faves2 = []
            for i in faves:
               faves2.append((i.name.encode('utf-8')))
            context = RequestContext(request, {'loggedin' : authenticated,'query': query,'result': result, 'added': food, 'removed': removefood,'favorites' : faves2})
            return HttpResponse(template.render(context))

        else:
            return HttpResponseRedirect('/accounts/login/')
    else:
        template = loader.get_template('search.html')
        authenticated = request.user.is_authenticated()
        context = RequestContext(request, {'loggedin' : authenticated})
        return HttpResponse(template.render(context))


def about(request):
    return render_to_response('users/about.html')



