from django.shortcuts import render_to_response
import cgi
import os
from models import Article,Idea,Person,Rating
from mongoengine import *
from django.http import HttpResponseRedirect, HttpResponseServerError
import random


def go(request):
	user = request.user
	rating = None
	if user.is_authenticated():
		people = Person.objects(email=request.user.email)
		if people and len(people)>0:
			person = people[0]			
		 	if person:
		 		pratings = Rating.objects().order_by('score')
		 		if pratings and len(pratings)>=0:
		 			for prating in pratings:
		 				if person.currentRating >= prating.score:
		 					rating = prating
		 					break
	
	template_values = {		
		'user' : user,
		'person' : person,
		'rating' : rating,
	}

	path = os.path.join(os.path.dirname(__file__), 'templates/ideas/mystats.html')
	return render_to_response(path, template_values)