from django.shortcuts import render_to_response
import cgi
from operator import itemgetter
import os
from models import Idea
from mongoengine import *
from django.http import HttpResponseRedirect, HttpResponseServerError
import random

def go(request):
	user = request.user
	
	filtertag =  request.META['HTTP_REFERER']
	showtag = False
	if filtertag.find('/tag/') >=0:
		showtag = True
		filtertag = filtertag.split('/')[4]
	else:
		filtertag = None
	
	
	ideas = None
	ideas = Idea.objects(isvisible=False).order_by('-votecount')
	s_ideas = []
	for idea in ideas:
		if str(request.user) in idea.voters:
			idea.hasvoted = True
		if showtag:
			if filtertag in idea.tags:
				s_ideas.append(idea)
		else:
			s_ideas.append(idea)

	
	template_values = {
		'ideas': s_ideas,
		'user' : user,
	}

	path = os.path.join(os.path.dirname(__file__), 'templates/ideas/archive.html')
	return render_to_response(path, template_values)