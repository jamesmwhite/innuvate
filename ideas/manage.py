from django.shortcuts import render_to_response
import cgi
import os
from models import Article,Idea
from mongoengine import *
from django.http import HttpResponseRedirect, HttpResponseServerError
import random


def go(request):
	user = request.user
				
	articles = None
	#articles = Article.objects(reported=True)
	articles = Article.objects(Q(reported=True) & Q(isvisible=True))
	s_articles = []
	for art in articles:
		s_articles.append(art)		
		
	ideas = None
	ideas = Idea.objects(Q(reported=True) & Q(isvisible=True))
	s_ideas = []
	for idea in ideas:		
		s_ideas.append(idea)


	promoted = Idea.objects(ispromoted=True)
	s_promoted = []
	for prom in promoted:
		s_promoted.append(prom)

	
	template_values = {
		'articles': s_articles,
		'ideas': s_ideas,
		'user' : user,
		'promoted': s_promoted,
	}

	path = os.path.join(os.path.dirname(__file__), 'templates/ideas/manage.html')
	return render_to_response(path, template_values)