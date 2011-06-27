from django.shortcuts import render_to_response
import cgi
from operator import itemgetter
import os
from models import Idea
from mongoengine import *
from django.http import HttpResponseRedirect, HttpResponseServerError
import random

class tagclass:
	tag = ''
	val = ''
	color = ''

def go(request):
	user = request.user
	
	tags = Idea.objects.item_frequencies('tags', normalize=True)
	top_tags = sorted(tags.items(), key=itemgetter(1), reverse=True)[:6]
	aaa = top_tags
	tagobs = []
	for key in top_tags:
		tg = tagclass()
		tg.tag = key[0]
		tg.val = key[1]
		tg.color = str(random.randrange(10,30,1))
		if len(tg.tag)>0:
			tagobs.append(tg)
	
	template_values = {
		'user' : user,
		'tags': tagobs,
		'aaa':aaa,
	}

	path = os.path.join(os.path.dirname(__file__), 'templates/ideas/tagcloud.html')
	return render_to_response(path, template_values)