from django.shortcuts import render_to_response
import cgi
import os
from models import Article
from mongoengine import *
from django.http import HttpResponseRedirect, HttpResponseServerError
import random

def go(request):
	user = request.user
		
	articles = None
	articles = Article.objects(isvisible=True).order_by('-votecount')
	s_articles = []
	for art in articles:
		if str(request.user) in art.voters:
			art.hasvoted = True
		s_articles.append(art)

	
	template_values = {
		'articles': s_articles,
		'user' : user,
	}

	path = os.path.join(os.path.dirname(__file__), 'templates/ideas/articles.html')
	return render_to_response(path, template_values)