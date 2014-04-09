from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse
import sys
import json

def index(request):
    #get today.json from parent directory
    file = open('../today.json')
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

def menu(request, menu):
    return HttpResponse("Here's today's menu:")
