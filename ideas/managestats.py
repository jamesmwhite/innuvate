from django.shortcuts import render_to_response
import cgi
import os
from models import Article,Idea,Stat
from mongoengine import *
from django.http import HttpResponseRedirect, HttpResponseServerError
import random


def go(request):
	user = request.user
				
	stats = Stat.objects()

	template_values = {
		'stats': stats,
		'user' : user,
	}

	path = os.path.join(os.path.dirname(__file__), 'templates/ideas/managestats.html')
	return render_to_response(path, template_values)