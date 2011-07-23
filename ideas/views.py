from mongoengine import *
from models import Idea,Comment,Article
from django.http import HttpResponseRedirect, HttpResponseServerError
import traceback
from django.core.signals import got_request_exception
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
import threading
import datetime



@login_required
def dostar(request):
	error_msg = u"No POST data sent."	
	if request.method == "POST":
		post = request.POST.copy()
		if post.has_key('id') :
			try:
				iid = post['id']
				ideas = Idea.objects(id=iid)
				if(len(ideas) >0):
					idea = ideas[0]
					idea.hasstar = True
					idea.save()
				return HttpResponseRedirect('/')
			except Exception as inst:
				return HttpResponseServerError('wowza! an error occurred, sorry!</br>'+str(inst))
		else:
			error_msg = u"Insufficient POST data (need 'slug' and 'title'!)"
	return HttpResponseServerError(error_msg)
	
@login_required
def report(request):
	tag =  request.path_info
	tag = tag.split('/')[2]
	ideas = Idea.objects(id=tag)
	if len(ideas)>0:
		idea = ideas[0]
		idea.reported = True
		idea.save()
	return HttpResponseRedirect('/')

@login_required	
def reportarticle(request):
	tag =  request.path_info
	tag = tag.split('/')[2]
	articles = Article.objects(id=tag)
	if len(articles)>0:
		art = articles[0]
		art.reported = True
		art.save()
	return HttpResponseRedirect('/')
	
@login_required
def voteart(request):
	error_msg = u"No POST data sent."	
	if request.method == "POST":
		post = request.POST.copy()
		if post.has_key('id') and post.has_key('vote'):
			try:
				iid = post['id']
				articles = Article.objects(id=iid)
				if(len(articles) >0):
					art = articles[0]
					curcount = art.votecount
					if post['vote']=='1':
						art.votecount = curcount + 1
					elif post['vote']=='3':
						art.votecount = curcount + 3
					elif post['vote']=='5':
						art.votecount = curcount + 5	
					art.voters.append(str(request.user))
					art.save()
				return HttpResponseRedirect('/')
			except Exception as inst:
				return HttpResponseServerError('wowza! an error occurred, sorry!</br>'+str(inst))
		else:
			error_msg = u"Insufficient POST data (need 'slug' and 'title'!)"
	return HttpResponseServerError(error_msg)
	
@login_required
def unpublish(request):
	error_msg = u"No POST data sent."	
	if request.method == "POST":
		post = request.POST.copy()
		if post.has_key('id') and post.has_key('type'):
			try:
				iid = post['id']
				type = post['type']
				if type =='idea':
					ideas = Idea.objects(id=iid)
					if(len(ideas) >0):
						idea = ideas[0]
						idea.isvisible = False						
						idea.save()
				else:
					articles = Article.objects(id=iid)
					if(len(articles) >0):
						art = articles[0]
						art.isvisible = False						
						art.save()
				return HttpResponseRedirect('/')
			except Exception as inst:
				return HttpResponseServerError('wowza! an error occurred, sorry!</br>'+str(inst))
		else:
			error_msg = u"Insufficient POST data (need 'slug' and 'title'!)"
	return HttpResponseServerError(error_msg)

@login_required	
def approve(request):
	error_msg = u"No POST data sent."	
	if request.method == "POST":
		post = request.POST.copy()
		if post.has_key('id') and post.has_key('type'):
			try:
				iid = post['id']
				type = post['type']
				if type =='idea':
					ideas = Idea.objects(id=iid)
					if(len(ideas) >0):
						idea = ideas[0]
						idea.reported = False
						idea.save()
				else:
					articles = Article.objects(id=iid)
					if(len(articles) >0):
						art = articles[0]
						art.reported = False						
						art.save()
				return HttpResponseRedirect('/')
			except Exception as inst:
				return HttpResponseServerError('wowza! an error occurred, sorry!</br>'+str(inst))
		else:
			error_msg = u"Insufficient POST data (need 'slug' and 'title'!)"
	return HttpResponseServerError(error_msg)
	
@login_required
def vote(request):
	error_msg = u"No POST data sent."	
	if request.method == "POST":
		post = request.POST.copy()
		print 'post = '+str(post)
		if post.has_key('id') and post.has_key('star1'):
			try:
				iid = post['id']
				ideas = Idea.objects(id=iid)
				if(len(ideas) >0):
					idea = ideas[0]
					curcount = idea.votecount
					print post['star1']
					voteval = int(post['star1'])		
					idea.votecount = idea.votecount + voteval
					idea.voters.append(str(request.user))
					idea.save()
				return HttpResponseRedirect('/')
			except Exception as inst:
				return HttpResponseServerError('wowza! an error occurred, sorry!</br>'+str(inst))
		else:
			error_msg = u"Insufficient POST data (need 'slug' and 'title'!)"
	return HttpResponseServerError(error_msg)
	
@staff_member_required	
def demote(request):
	error_msg = u"No POST data sent."	
	if request.method == "POST":
		post = request.POST.copy()
		if post.has_key('id') :
			try:
				iid = post['id']
				ideas = Idea.objects(id=iid)
				if(len(ideas) >0):
					idea = ideas[0]
					idea.ispromoted = False
					idea.save()
				return HttpResponseRedirect('/')
			except Exception as inst:
				return HttpResponseServerError('wowza! an error occurred, sorry!</br>'+str(inst))
		else:
			error_msg = u"Insufficient POST data (need 'slug' and 'title'!)"
	return HttpResponseServerError(error_msg)
	
@staff_member_required	
def promote(request):
	error_msg = u"No POST data sent."	
	if request.method == "POST":
		post = request.POST.copy()
		print "promote ID: "+post['id']
		if post.has_key('id') :
			try:
				iid = post['id']
				ideas = Idea.objects(id=iid)
				print "len: "+str(len(ideas))
				if(len(ideas) >0):
					idea = ideas[0]
					idea.ispromoted = True
					idea.save()
				return HttpResponseRedirect('/')
			except Exception as inst:
				return HttpResponseServerError('wowza! an error occurred, sorry!</br>'+str(inst))
		else:
			error_msg = u"Insufficient POST data (need 'slug' and 'title'!)"
	return HttpResponseServerError(error_msg)

@login_required    
def addcomment(request):
	error_msg = u"No POST data sent."
	print 'addcomment called'	
	if request.method == "POST":
		post = request.POST.copy()
		if post.has_key('content') and post.has_key('id'):
			try:
				iid = post['id']
				ideas = Idea.objects(id=iid)
				if(len(ideas) >0):
					idea = ideas[0]
					comment = Comment()
					comment.content = post['content']
					comment.author = str(request.user)
					idea.comments.append(comment)
					idea.save()
					try:
						t = ThreadClass(comment.author+' has commented on your idea: '+idea.title, comment.author+' commented: '+comment.content,[idea.email])
						t.start()					
					except Exception as inst:
						print 'exception sending email '+str(inst)
				return HttpResponseRedirect('/')
			except Exception as inst:
				return HttpResponseServerError('wowza! an error occurred, sorry!</br>'+str(inst))
		else:
			error_msg = u"Insufficient POST data (need 'slug' and 'title'!)"
	return HttpResponseServerError(error_msg)
 
@login_required    
def submitidea(request):
	error_msg = u"No POST data sent."	
	if request.method == "POST":
		post = request.POST.copy()
		if post.has_key('tags') and post.has_key('title') and post.has_key('content'):
			try:
				content = post['content']
				idea = Idea()
				idea.tags = post['tags'].strip().split(',')
				idea.author = str(request.user)
				print "user: "+str(request.user)
				idea.email = str(request.user.email)
				idea.title = post['title']
				idea.votecount = 0
				idea.viewcount = 0
				idea.content = content
				if idea.content and idea.title and idea.author:
					try:
						idea.save()
					except Exception as inst:
						print inst
				return HttpResponseRedirect('/')
			except:
				return HttpResponseServerError('wowza! an error occurred, sorry!')
		else:
			error_msg = u"Insufficient POST data (need 'content' and 'title'!)"
	return HttpResponseServerError(error_msg)

@login_required	
def submitarticle(request):
	error_msg = u"No POST data sent."	
	if request.method == "POST":
		post = request.POST.copy()
		if post.has_key('tags') and post.has_key('title') and post.has_key('url'):
			try:
				url = post['url']
				art = Article()
				art.tags = post['tags'].strip().split(',')
				art.author = str(request.user)
				art.title = post['title']
				art.votecount = 0
				art.viewcount = 0
				if not url.startswith('http://'):
					url = 'http://'+url
				art.url = url
				if art.url and art.title and art.author:
					try:
						art.save()
					except Exception as inst:
						print inst
				return HttpResponseRedirect('/')
			except:
				return HttpResponseServerError('wowza! an error occurred, sorry!')
		else:
			error_msg = u"Insufficient POST data (need 'content' and 'title'!)"
	return HttpResponseServerError(error_msg)
	
def pp(sender, **kwargs):
    print sys.stderr, ''.join(traceback.format_exception(*sys.exc_info()))

@login_required    
def update_idea(request, slug):
    if request.method == "POST":
    	connect('innovation')
        post = request.POST.copy()
        #idea = Idea.objects.get(slug=slug)
        post = None
        for idea in Idea.objects(id=id):
        	post = idea	
        if post.has_key('slug'):
            slug_str = post['slug']
            if idea.slug != slug_str:
                if Idea.objects.filter(slug=slug_str).count() > 0:
                    error_msg = u"Slug already taken."
                    return HttpResponseServerError(error_msg)
                idea.slug = slug_str
        if post.has_key('title'):
            idea.title = post['title']
        if post.has_key('text'):
            idea.text = post['text']
        idea.save()
        return HttpResponseRedirect(idea.get_absolute_url())
    error_msg = u"No POST data sent."
    return HttpResponseServerError(error_msg)
   
   

        
class ThreadClass(threading.Thread):
	body = ''
	to = ''
	subject = ''
	def __init__(self,subject,body,to):
		threading.Thread.__init__(self)
		self.subject = subject
		self.body = body
		self.to = to
	def run(self):
		#print 'emailing: '+self.subject+' '+self.body+' '+str(self.to)
		try:
			send_mail(subject, body, 'update@donotreply.com',[to], fail_silently=False)
		except:
			print 'error sending mail in thread'
