from django.shortcuts import render_to_response
import cgi
import os
from models import Idea,Rating,Person
from mongoengine import *
from django.http import HttpResponseRedirect, HttpResponseServerError
from django.contrib.auth.decorators import user_passes_test
import registration.urls
from django.contrib.auth.models import User
from django.db import models
import views

#@user_passes_test(lambda u: u.has_perm('polls.can_vote'))
def go(request):
	
	tabselected = None
	filtertag = request.META['PATH_INFO']
	if filtertag.find('/idea/') >= 0:
		filtertag = filtertag[6:]
		tabselected = filtertag.replace('/', '')
#		tabselected = 4
	else:
		filtertag = None
		
 	user = request.user
 	
 	rating = None
 	if user.is_authenticated():
 		print 'AAAA'
	 	person = views.getPerson(request)
	 	if person:
	 		pratings = Rating.objects().order_by('score')
	 		if pratings and len(pratings)>=0:
	 			for prating in pratings:
	 				if person.currentRating >= prating.score:
	 					rating = prating
	 					break
 		
 	
	template_values = {
 		'user':user,
 		'tabselected':tabselected,
 		'filtertag':None,
 		'rating':rating,
	}
	path = os.path.join(os.path.dirname(__file__), 'templates/ideas/index.html')
	return render_to_response(path, template_values)
