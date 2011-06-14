from django.conf.urls.defaults import patterns, include, url
from django.conf import settings


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
    (r'^', include('innov9.ideas.urls')),
    # Examples:
    # url(r'^$', 'innov9.views.home', name='home'),
    # url(r'^innov9/', include('innov9.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    # (r'^accounts/login/$',  login),
	#(r'^accounts/logout/$', logout),
	(r'^accounts/', include('registration.urls')),
)
