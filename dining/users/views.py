from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from users.models import NetID
import sys
import json

#david experiment
from django.template.loader import get_template
from django.template import Context # for inserting data from our view in correct place
import sqlite3 as lite
from django.views.generic.base import TemplateView # a view that knows how to display a template
from users.models import NetID 
from django.shortcuts import render_to_response
#from django.config import settings

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
    for dic in today: 
        menu.append((dic['dhall'], dic['meal'], dic['menus']))
    template = loader.get_template('users/index.html')
    context = RequestContext(request, {'menu' : menu})
    if request.method == 'POST':
        food = request.POST.get('addItem')
        if request.user.is_authenticated():
            idy = request.user.get_username()
            person = NetID.objects.filter(netid = idy)
            faves = list(person[0].favorites.all())
            faves.append("you just added:")
            faves.append(food)
            #faves = [food]

            template = loader.get_template('users/favorites.html')
            context = RequestContext(request, {'netid': request.user.get_username(), 'f\
avorites':faves})
            return HttpResponse(template.render(context))
        else:
                  return HttpResponseRedirect('/accounts/login/')

    return HttpResponse(template.render(context))
    


def favorites(request):
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
        context = RequestContext(request, {'netid': request.user.get_username(), 'favorites':faves})
        return HttpResponse(template.render(context))
    else:
        #return HttpRequest(urljoin(settings.CAS_SERVER_URL, 'login'))
        return HttpResponseRedirect('/accounts/login/')
        #return HttpResponse('<html>Please <a href="http://tigerbites.org/accounts/login">sign in</a> to a CAS authenticated account before viewing or changing favorite dining items')
        #return HttpResponse('<html>we should redirect people that aren\'t signed in to the cas login')




def search(request):
    if 's1' in request.GET:
        #message = 'You searched for: %r' %request.GET['s1']
        #return HttpResponse(message)
        query = request.GET['s1']
        template = loader.get_template('search.html')
        context = RequestContext(request, {'query': query})
        return HttpResponse(template.render(context))
    return render_to_response('search.html')

def suggestions(request):
    return render_to_response('suggestions.html')


#def add_item(request, item_name = ''):
 #   if request.user.is_authenticated():
  #      name = request.user.get_username()
   #     try:
    #        person = NetID.objects.get(netid = name)
     #   except NetID.DoesNotExist:
      #      person = NetID(netid = name)
       #     person.save()
        #item = Item.objects.get(name = item_name)
        #person.favorites.add(item)
        #context = load_index_context(request)
        #return HttpResponse(template.render(context))
            

    # first check that item_name is in the list, else raise error
    # 
 #   Users.object.get(netid = 
    


# david's experiment 
#def favorites(request):                                                               
#    name = 'Duguuu'          
#    html = '<html><body>Yo, what up %s, you are ugly</body></html>' %name 
#    return HttpResponse(html)  
                              
#def favorites(request, user_id=2):
#    return render_to_response('favorite.html',
#                              {'userFavorites': NetID.objects.get(id=user_id)})

#class FavoritesTemplate(TemplateView):
 #   template_name = 'favorites_template.html'
#
 #   def get_context_data(self, **kwargs):
  #      context = super(FavoritesTemplate, self).get_context_data(**kwargs)
   #     context['name'] = 'Lisa and Diogo'
    #    retu
