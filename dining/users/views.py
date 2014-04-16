from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse
import sys
import json

#david experiment
from django.template.loader import get_template
from django.template import Context # for inserting data from our view in correct place
import sqlite3 as lite
from django.views.generic.base import TemplateView # a view that knows how to display a template
from users.models import NetID 
from django.shortcuts import render_to_response

def index(request):
    #get today.json from parent directory
    
    file = open('/home/ubuntu/TigerBites/dining/today.json')
    today = json.load(file)
    file.close()
    # pass arguments to template of menu that makes sense. 
    # may likely just be list of menu items as ROMA_LUNCH
   # items_only = []
    #for dhall_and_meal in today:
     #   for item in dhall_and_meal['menus']:
      #      items_only.append(item[        
    menus = today
    template = loader.get_template('users/index.html')
    context = RequestContext(request, {'menus': menus})
    return HttpResponse(template.render(context))

def menu(request):
    return HttpResponse("Here's today's menu:")

# david's experiment
#def favorites(request):
#    name = 'Duguuu'
#    html = '<html><body>Yo, what up %s, you are ugly</body></html>' %name
#    return HttpResponse(html)
    
def favorites(request):
    #name = 'Lisa and Diogo'
    #t = get_template('favorites.html')
    #html = t.render(Context({'name': name})) #'listOfThings': listOfThings}))
    #return HttpResponse(html)
    netid = request.user.get_username()
    template = loader.get_template('users/favorite.html')
    context = RequestContext(request, {'netid': netid})
    return render_to_response('favorites.html')
                              
#def favorites(request, user_id=2):
#    return render_to_response('favorite.html',
#                              {'userFavorites': NetID.objects.get(id=user_id)})

#class FavoritesTemplate(TemplateView):
 #   template_name = 'favorites_template.html'
#
 #   def get_context_data(self, **kwargs):
  #      context = super(FavoritesTemplate, self).get_context_data(**kwargs)
   #     context['name'] = 'Lisa and Diogo'
    #    return context
