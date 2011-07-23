from django.db import models
from django.contrib.auth.models import User
from mongoengine import *
from django.db.models.signals import post_save
from django.contrib import admin
import datetime

def create_user_profile(sender, **kwargs):		
    """When creating a new user, make a profile for him or her."""
    u = kwargs["instance"]
    if not UserProfile.objects.filter(user=u):
        UserProfile(user=u).save()

post_save.connect(create_user_profile, sender=User)

class Comment(EmbeddedDocument):	
	content = StringField(required=True)
	votecount = IntField()
	#ideakey = StringField(required=True)
	author = StringField(required=True)
	date = DateTimeField(default=datetime.datetime.now)

class Article(Document):
	tags = ListField(StringField(max_length=30))
	date = DateTimeField(default=datetime.datetime.now)
	title = StringField(required=True)
	url = StringField(required=True)
	author = StringField()
	hasvoted = False
	votecount = IntField()
	viewcount = IntField()
	voters = ListField(StringField())
	reported = BooleanField(default=False) 
	isvisible = BooleanField(default=True)
	
class Idea(Document):
	comments = ListField(EmbeddedDocumentField(Comment))
	author = StringField(required=True)
	content = StringField(required=True)	
	title = StringField(required=True)
	email = StringField(default="")
	votecount = IntField()
	groupKey = StringField()	
	voters = ListField(StringField())
	hasvoted = False
	tags = ListField(StringField(max_length=30))
	date = DateTimeField(default=datetime.datetime.now)
	hasstar = BooleanField(default=False)
	reported = BooleanField(default=False) 
	isvisible = BooleanField(default=True)
	ispromoted = BooleanField(default=False) 
	viewcount = IntField() 

	@queryset_manager
	def objects(doc_cls, queryset):
		return queryset.order_by('-date')
		
	@queryset_manager
	def byvote(doc_cls, queryset):
		return queryset.order_by('votecount')
		
	
class Group():
	name = StringField(required=True)
	managerKey = StringField(required=True)

class UserProfile(models.Model):
    posts = models.IntegerField(default=0)
    user = models.ForeignKey(User, unique=True)

    def __unicode__(self):
        return unicode(self.user)
        
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user"]

class ForumAdmin(admin.ModelAdmin):
    pass

class ThreadAdmin(admin.ModelAdmin):
    list_display = ["title", "forum", "creator", "created"]
    list_filter = ["forum", "creator"]

class PostAdmin(admin.ModelAdmin):
    search_fields = ["title", "creator"]
    list_display = ["title", "thread", "creator", "created"]