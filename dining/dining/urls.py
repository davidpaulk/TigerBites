from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^menus/', include('users.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^accounts/login/$', 'django_cas.views.login'),
                       url(r'^accounts/logout/$', 'django_cas.views.logout'),
)
    # Examples:
    # url(r'^$', 'dining.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

#    url(r'^admin/', include(admin.site.urls)),
#)
