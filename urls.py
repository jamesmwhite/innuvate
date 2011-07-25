from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from registration.views import register
from ideas.registration.register import InnuvateRegistrationForm

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
	(r'^', include('innuvate.ideas.urls')),

	url(r'^admin/', include(admin.site.urls)),
	# (r'^accounts/login/$',  login),
	#(r'^accounts/logout/$', logout),
	url(r'^accounts/profile/$', 'ideas.idea_main.go'),
	
	url(r'^accounts/register/$',register,{'form_class' : InnuvateRegistrationForm},name='registration_register'),
	(r'^accounts/', include('registration.urls')),
)
