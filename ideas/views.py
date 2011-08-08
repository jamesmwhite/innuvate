from mongoengine import *
from models import Idea,Comment,Article,Person,Score,Stat,Rating
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
		incrementStat('ideasreported',1)
		person = getPerson(request)
		if person:
			person.timesReport = person.timesReport +1
			rating = Score.objects(type='report')[0].value
			person.currentRating = person.currentRating + rating
			person.save()
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
		incrementStat('articlesreported',1)
		person = getPerson(request)
		if person:
			person.timesReport = person.timesReport +1
			rating = Score.objects(type='report')[0].value
			person.currentRating = person.currentRating + rating
			person.save()
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
					incrementStat('unique_article_votes',1)
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
						try:
							t = ThreadClass("Idea Unpublished", "Your idea '"+idea.title +"' has been unpublished.",[idea.email]+"'")
							t.start()					
						except Exception as inst:
							print 'exception sending email '+str(inst)
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
					incrementStat('unique_idea_votes',1)
					incrementStat('total_idea_vote_count',voteval)
					person = getPerson(request)
					if person:
						person.lastActive = datetime.datetime.now()
						rating = Score.objects(type='vote')[0].value
						person.currentRating = person.currentRating + rating
						person.timesVoted = person.timesVoted + 1
						person.save()
					idea.save()
					try:
						t = ThreadClass("Idea voted on", "Your idea '"+idea.title +"' has been given a voting of "+str(voteval)+".",[idea.email])
						t.start()					
					except Exception as inst:
						print 'exception sending email '+str(inst)
				return HttpResponseRedirect('/')
			except Exception as inst:
				return HttpResponseServerError('wowza! an error occurred, sorry!</br>'+str(inst))
		else:
			print 'no vote cast, no stars selected'
#			error_msg = u"Insufficient POST data (need 'slug' and 'title'!)"
			return HttpResponseRedirect('/')
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
					incrementStat('promotions',1)
					people = Person.objects(email=idea.email)
					if people and len(people)>0:
						person = people[0]
						person.timesPromoted = person.timesPromoted +1
						rating = Score.objects(type='promotion')[0].value
						person.currentRating = person.currentRating + rating
						person.save()
					idea.save()
					try:
						t = ThreadClass("Idea Promoted", "Your idea '"+str(idea.title)+"' has been promoted and will now go forward for idea selection, it may or may not be chosen for implementation.",[idea.email])
						t.start()					
					except Exception as inst:
						print 'exception sending email '+str(inst)
						traceback.print_exc()
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
					if not comment.content or comment.content.strip()=="":
						return HttpResponseRedirect('/')
					comment.author = str(request.user)
					idea.comments.append(comment)
					incrementStat('comments',1)
					person = getPerson(request)
					if person:
						person.lastActive = datetime.datetime.now()
						person.timesCommented = person.timesCommented + 1
						rating = Score.objects(type='comment')[0].value
						person.currentRating = person.currentRating + rating
						person.save()
					idea.save()
					try:
						t = ThreadClass(comment.author+" has commented on your idea: '"+idea.title+"'", comment.author+" commented: '"+comment.content+"'",[idea.email])
						t.start()					
					except Exception as inst:
						print 'exception sending email '+str(inst)
				return HttpResponseRedirect('/')
			except Exception as inst:
				return HttpResponseServerError('wowza! an error occurred, sorry!</br>'+str(inst))
		else:
			print 'didnt comment, no data'
			return HttpResponseRedirect('/')
#			error_msg = u"Insufficient POST data (need 'slug' and 'title'!)"

	return HttpResponseServerError(error_msg)
 
@login_required    
def submitidea(request):
	error_msg = u"No POST data sent."	
	if request.method == "POST":
		post = request.POST.copy()
		if post.has_key('tags') and post.has_key('title') and post.has_key('content'):
			try:	
				content = post['content']
				title = post['title']
				idea = Idea()
				alltag =  post['tags']
				print 'submitting idea: '+title
				print 'user: '+str(request.user)
				print content
				alltag = alltag.strip()
				tags = None
				if alltag.find(',') >=0:
					tags = alltag.split(',')
				if tags:
					idea.tags = tags
				else:
					if alltag.find(' ')>=0:
						tags = alltag.split(' ')
						idea.tags =  tags
					else:
						tags = [alltag]
						idea.tags =  tags
				idea.title = title
				idea.author = str(request.user)
				print "user: "+str(request.user)
				idea.email = str(request.user.email)
				
				idea.votecount = 0
				idea.viewcount = 0
				idea.content = content
				if idea.content and idea.title and idea.author:
					try:
						person = getPerson(request)
						person.timesIdea = person.timesIdea + 1
						person.lastActive = datetime.datetime.now()
						rating = Score.objects(type='submitidea')[0].value
						person.currentRating = person.currentRating + rating
						person.save()
						incrementStat('ideas',1)
						idea.save()
					except Exception as inst:
						print inst
						traceback.print_exc()
				return HttpResponseRedirect('/')
			except Exception as inst:
				return HttpResponseServerError('wowza! an error occurred, sorry!'+str(inst))
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
				alltag =  post['tags']
				print 'submitting article: '+post['title']
				print 'user: '+str(request.user)
				print url
				alltag = alltag.strip()
				tags = None
				if alltag.find(',') >=0:
					tags = alltag.split(',')
				if tags:
					art.tags = tags
				else:
					if alltag.find(' ')>=0:
						tags = alltag.split(' ')
						art.tags =  tags
					else:
						tags = [alltag]
						art.tags =  tags
				art.author = str(request.user)
				art.title = post['title']
				art.votecount = 0
				art.viewcount = 0
				if not url.startswith('http://'):
					url = 'http://'+url
				art.url = url
				if art.url and art.title and art.author:
					try:
						person = getPerson(request)
						person.timesArticle = person.timesArticle + 1
						person.lastActive = datetime.datetime.now()
						rating = Score.objects(type='submitarticle')[0].value
						person.currentRating = person.currentRating + rating
						person.save()
						incrementStat('articles',1)
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
   
        
def incrementStat(statname,value):
	stats = Stat.objects(name=statname)
	stat = None
	if not stats or len(stats)<=0:
		stat = Stat()
		stat.name = statname
		stat.total = 0
	else:
		stat = stats[0]
	stat.total = stat.total + value
	stat.save()
	        
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
			send_mail(self.subject, self.body, 'innUvate@donotreply.com',self.to, fail_silently=False)
		except Exception as excep:
			print 'error sending mail in thread '+str(excep)
			
@login_required			
def getPerson(request):
	people = Person.objects(email=str(request.user.email))
	if people and len(people)>0:
		person = people[0]
		return person
	return None
	
@login_required	
def initialiseScoring(request):
	score = Score.objects(type='submitidea')
	if not score:
		score = Score()
		score.type='submitidea'
		score.value=100
		score.save()
	
	score = Score.objects(type='submitarticle')
	if not score:
		score = Score()
		score.type='submitarticle'
		score.value=80
		score.save()
	
	score = Score.objects(type='comment')
	if not score:
		score = Score()
		score.type='comment'
		score.value=50
		score.save()
	
	score = Score.objects(type='vote')
	if not score:
		score = Score()
		score.type='vote'
		score.value=40
		score.save()

	score = Score.objects(type='report')
	if not score:
		score = Score()
		score.type='report'
		score.value=20
		score.save()
	
	score = Score.objects(type='view')
	if not score:
		score = Score()
		score.type='view'
		score.value=10
		score.save()
	
	score = Score.objects(type='promotion')
	if not score:
		score = Score()
		score.type='promotion'
		score.value=80
		score.save()
		
	initialiseRatings()
	return HttpResponseRedirect('/')

def initialiseRatings():
	rating = Rating.objects(name='Squire')
	if not rating:
		rating = Rating()
		rating.score = 0
		rating.name = 'Squire'
		rating.image = '/media/images/squire.png'
		rating.save()
	
	rating = Rating.objects(name='Baron')
	if not rating:
		rating = Rating()
		rating.score = 1000
		rating.name = 'Baron'
		rating.image = '/media/images/baron.png'
		rating.save()
	
	rating = Rating.objects(name='Count')
	if not rating:
		rating = Rating()
		rating.score = 1500
		rating.name = 'Count'
		rating.image = '/media/images/count.png'
		rating.save()
		
	rating = Rating.objects(name='Duke')
	if not rating:
		rating = Rating()
		rating.score = 3000
		rating.name = 'Duke'
		rating.image = '/media/images/duke.png'
		rating.save()
		
	rating = Rating.objects(name='Prince')
	if not rating:
		rating = Rating()
		rating.score = 5000
		rating.name = 'Prince'
		rating.image = '/media/images/prince.png'
		rating.save()
		
	rating = Rating.objects(name='Archduke')
	if not rating:
		rating = Rating()
		rating.score = 6000
		rating.name = 'Archduke'
		rating.image = '/media/images/archduke.png'
		rating.save()
		
	rating = Rating.objects(name='Grand Duke')
	if not rating:
		rating = Rating()
		rating.score = 7000
		rating.name = 'Grand Duke'
		rating.image = '/media/images/grandduke.png'
		rating.save()
		
	rating = Rating.objects(name='Viceroy')
	if not rating:
		rating = Rating()
		rating.score = 8000
		rating.name = 'Viceroy'
		rating.image = '/media/images/viceroy.png'
		rating.save()
		
	rating = Rating.objects(name='King')
	if not rating:
		rating = Rating()
		rating.score = 9000
		rating.name = 'King'
		rating.image = '/media/images/king.png'
		rating.save()
		
	rating = Rating.objects(name='Emperor')
	if not rating:
		rating = Rating()
		rating.score = 10000
		rating.name = 'Emperor'
		rating.image = '/media/images/emperor.png'
		rating.save()
		
def initIdeas(request):
	for i in range(100):
		idea = Idea()
		idea.title = "idea "+str(i)
		idea.content = "This is a test Idea"
		idea.author = "jimmy"
		idea.save()
	return HttpResponseRedirect('/')