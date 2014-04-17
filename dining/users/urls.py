from django.conf.urls import patterns, url, include
from users.views import *


urlpatterns = patterns('', 
                       url(r'^$', index, name = 'index'),
                       #url(r'^add/(?P<item_name>\w+)/$', 'add_item'),
                       #url(r'^add/(?P<item_name>\w+)/$', views.add), 
                       #url(r'^menu/', views.menu, name = 'menu'),
                       #david experiment
                       #url(r'^favorites/$', views.menu, name = 'favorites'),
                       #url(r'^get/(?P<users_id>\s+)/$', 'users.views.favorites'),
                       #url(r'^all/$', 'users.views.favorites'),
                       #url(r'^favorites_class_view/$', views.menu, name = 'favorites_class')
                       )
