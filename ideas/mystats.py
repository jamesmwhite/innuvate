from django.shortcuts import render_to_response
import cgi
import os
from models import Article,Idea,Person
from mongoengine import *
from django.http import HttpResponseRedirect, HttpResponseServerError
import random


def go(request):
	user = request.user
				
	if user.is_authenticated():
		people = Person.objects(email=request.user.email)
		if people and len(people)>0:
			person = people[0]
	
	template_values = {		
		'user' : user,
		'person' : person,		
	}

	path = os.path.join(os.path.dirname(__file__), 'templates/ideas/mystats.html')
	return render_to_response(path, template_values)