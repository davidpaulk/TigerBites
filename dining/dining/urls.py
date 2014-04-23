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
                       url(r'^suggestions/$', 'users.views.suggestions'),
                       url(r'^add/$', 'users.views.add'),
                       #url(r'^add/$', users.views.add_item),
                       #url(r'^favorites_class_view/$', FavoritesTemplate.as_view()),
                       # david experiment
                       #(r'^users/', include('users.urls')),
                       #url(r'^all/$', 'users.views.favorites'),
                       #url(r'^get/(?P<user_id>\d+)/$', 'users.views.favorites'),
)
    # Examples:
    # url(r'^$', 'dining.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

#    url(r'^admin/', include(admin.site.urls)),
#)
