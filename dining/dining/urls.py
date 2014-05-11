from django.conf.urls import patterns, include, url
#from users.views import FavoritesTemplate
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       (r'^$', include('users.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^accounts/login/$', 'django_cas.views.login'),
                       url(r'^accounts/logout/$', 'django_cas.views.logout'),
                       url(r'^add/(?P<item_name>\w+)/$', 'add_item'),
                       url(r'^favorites/$', 'users.views.favorites'),
                       url(r'^search/$', 'users.views.search'),
                       url(r'^about/$', 'users.views.about'),
                     
)

