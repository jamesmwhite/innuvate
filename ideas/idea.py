from django.shortcuts import render_to_response
import cgi
from operator import itemgetter
import os
from models import Idea
import views
from mongoengine import *
from django.http import HttpResponseRedirect, HttpResponseServerError
import random

class tagclass:
	tag = ''
	val = ''
	color = ''

def go(request):
	
	views.incrementStat('ideaviews',1)
	pathinfo = request.META['PATH_INFO']
	pathinfo = pathinfo[10:]
	pathinfo = pathinfo.replace('/','')
	
	user = request.user
	ideas = None
	idea = None
	try:
#		ideas = Idea.objects(Q(isvisible=True) & Q(ispromoted=False)).order_by('-votecount')[:20]
		ideas = Idea.objects(Q(isvisible=True) & Q(ispromoted=False) & Q(id=pathinfo)).order_by('-votecount')[:20]
	except:
		ideas = Idea.objects(Q(isvisible=True) & Q(ispromoted=False)).order_by('-votecount')[:20]
	if ideas == None or len(ideas) == 0:
		ideas = Idea.objects(Q(isvisible=True) & Q(ispromoted=False)).order_by('-votecount')[:20]
	if len(ideas)>0:
		idea = ideas[0]
		vc = idea.viewcount
		if str(user) in idea.voters:
			idea.hasvoted = True
		if vc==None:
			vc = 1
		else:
			vc = vc + 1
		idea.viewcount = vc
		idea.save()

	template_values = {
		'idea': idea,
		'user' : user,
	}

	path = os.path.join(os.path.dirname(__file__), 'templates/ideas/idea.html')
	return render_to_response(path, template_values)
