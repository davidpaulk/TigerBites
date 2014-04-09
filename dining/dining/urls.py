from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^users/', include('users.urls')),
                       url(r'^admin/', include(admin.site.urls)),
)
    # Examples:
    # url(r'^$', 'dining.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

#    url(r'^admin/', include(admin.site.urls)),
#)
