from django.shortcuts import render
from django.http import HttpResponse
import sys
import json

def index(request):
    #get today.json from parent directory
    file = open('today.json')
    today = json.load(file)
    file.close()
        global today
    file = open('today.json')
    today = json.load(file)
    file.close()
    # pass arguments to template of menu that makes sense. 
    # may likely just be list of menu items as ROMA_LUNCH
    menus = today
    template = loader.get_template('users/index.html')
    context = RequestContext(request, {'menus': menus})
    return HttpResponse(template.render(context))

def dhall(request, menu):
    return HttpResponse("Here's today's menu")


# Create your views here.
