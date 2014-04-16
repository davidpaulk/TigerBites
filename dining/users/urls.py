from django.conf.urls import patterns, url, include
from users import views


urlpatterns = patterns('', 
                       url(r'^$', views.index, name = 'index'),
                       url(r'^menu/', views.menu, name = 'menu'),
                       #david experiment
                       url(r'^favorites/$', views.menu, name = 'favorites'),
                       url(r'^get/(?P<users_id>\s+)/$', 'users.views.favorites'),
                       url(r'^all/$', 'users.views.favorites'),
                       #url(r'^favorites_class_view/$', views.menu, name = 'favorites_class')
                       )
