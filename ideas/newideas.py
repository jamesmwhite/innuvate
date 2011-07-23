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
	
	ideas = None
	ideas = Idea.objects(Q(isvisible=True) & Q(ispromoted=False)).order_by('-date')
	s_ideas = []
	for idea in ideas:
		s_ideas.append(idea)

	
	template_values = {
		'ideas': s_ideas,
		'user' : user,
	}

	path = os.path.join(os.path.dirname(__file__), 'templates/ideas/newideas.html')
	return render_to_response(path, template_values)