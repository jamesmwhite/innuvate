from django.conf.urls.defaults import *
from models import Idea
from mongoengine import *




urlpatterns = patterns(
    '',
    (r'^tag/.+/$','ideas.idea_main.go'),
    (r'^report/.+/$','ideas.views.report'),
	(r'^reportarticle/.+/$','ideas.views.reportarticle'),
    (r'^submitidea/$','ideas.views.submitidea'),
    (r'^submitarticle/$','ideas.views.submitarticle'),
    (r'^addcomment/$','ideas.views.addcomment'),
    (r'^dostar/$','ideas.views.dostar'),
    (r'^vote/$','ideas.views.vote'),
    (r'^promote/$','ideas.views.promote'),
    (r'^demote/$','ideas.views.demote'),
	(r'^unpublish/$','ideas.views.unpublish'),
	(r'^approve/$','ideas.views.approve'),
    (r'^voteart/$','ideas.views.voteart'),
    (r'^idea/.+/$','ideas.idea_main.go'),
    (r'^ideaview/.+/$','ideas.idea.go'),
	(r'^$',
     'ideas.idea_main.go'),
     (r'^topten$',
     'ideas.topten.go'),
     (r'^archive$',
     'ideas.archive.go'),
     (r'^tagcloud$',
     'ideas.tagcloud.go'),
     (r'^allideas$',
     'ideas.allideas.go'),
     (r'^articles$',
     'ideas.articles.go'),
	 (r'^manage$',
     'ideas.manage.go'),
	 (r'^tandc$',
     'ideas.tandc.go'),
	(r'^help$',
     'ideas.help.go'),
)
