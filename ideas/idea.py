from django.shortcuts import render_to_response
import cgi
from operator import itemgetter
import os
from models import Idea,Score
import views
from mongoengine import *
from django.http import HttpResponseRedirect, HttpResponseServerError
import random
import threading

class tagclass:
	tag = ''
	val = ''
	color = ''
	
class ThreadClass(threading.Thread):
	def __init__(self,request):
		threading.Thread.__init__(self)
		self.request = request
	def run(self):
		try:
			person = views.getPerson(self.request)
			if person:
				person.timesViewed = person.timesViewed + 1
				rating = Score.objects(type='view')[0].value
				person.currentRating = person.currentRating + rating
				person.save()
		except Exception as excep:
			print 'error updating ratings in thread '+str(excep)

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
		
		if user.is_authenticated():
			try:
				t = ThreadClass(request)
				t.start()					
			except Exception as inst:
				print 'exception updating view rating '+str(inst)
		
	template_values = {
		'idea': idea,
		'user' : user,
	}

	path = os.path.join(os.path.dirname(__file__), 'templates/ideas/idea.html')
	return render_to_response(path, template_values)


