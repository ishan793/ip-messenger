from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render_to_response
from forms import SignUpForm
from django.core.context_processors import csrf
from chatapp.models import *
import json
import datetime,time

#time = int(datetime.datetime.now().strftime("%s")) * 1000

def encodeToJson(data):
	return '{"fields": ' + json.dumps(list(data.values()), cls=DjangoJSONEncoder) + "}"
	
def Authenticate(request):
	tim=time.mktime(datetime.datetime.now().timetuple()) * 1000
	if request.REQUEST.has_key('u_name') == True:
		
		if(SignUp.objects.filter(user_name=request.REQUEST['u_name']) and SignUp.objects.filter(password=request.REQUEST['pass'])):
			data=encodeToJson({"auth":1,"time":tim})
			
			return HttpResponse(data, mimetype = "application/json")
		elif(not len(SignUp.objects.filter(user_name=request.REQUEST['u_name']))):
			data=encodeToJson({"auth":2})
			
			return HttpResponse(data, mimetype = "application/json")
		else:
			data=encodeToJson({"auth":0})			
			return HttpResponse(data, mimetype = "application/json")

## Create view for the sign up page.
def register_user(request):
	if request.POST:
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			
			return HttpResponseRedirect('/success/')
			
	else:
		form = SignUpForm()
		
	args = {}
	args.update(csrf(request))
	
	args['form'] = form
	
	return render_to_response('register.html', args)


def save_to_onpre():
	signdata=SignUp.objects.all()
	predata=OnlinePresence.objects.all()
	ls=[]
	if(len(predata)>0):
		for d in predata:
			ls.append(d.user_name)
		for d in signdata:
			if(d.user_name in ls):
				continue
			else:
				online_pre=OnlinePresence(user_name=d.user_name,presence=1,ping_time=time.mktime(datetime.datetime.now().timetuple()) * 1000)
				online_pre.save()
	else:
		for d in signdata:
			online_pre=OnlinePresence(user_name=d.user_name,presence=1,ping_time=time.mktime(datetime.datetime.now().timetuple()) * 1000)
			online_pre.save()

	
## To be activated when registration is successful.
def register_success(request):
	save_to_onpre()
	return render_to_response('register_success.html')

	
	
def online_presence(request):
	if request.REQUEST.has_key('u_name') == True:
		if(SignUp.objects.filter(user_name=request.REQUEST['u_name']) and SignUp.objects.filter(password=request.REQUEST['pass'])):
			d=OnlinePresence.objects.get(user_name=request.REQUEST['u_name'])
			print d.presence,d.user_name,d.ping_time
			d.user_name=request.REQUEST['u_name']
			d.presence=1
			d.ping_time=time.mktime(datetime.datetime.now().timetuple()) * 1000
			d.save()
			
	return online_users()

def online_users():
	data=OnlinePresence.objects.all()
	
	return HttpResponse(encodeToJson(data), mimetype = "application/json")

def flush_all_presence(request):
	if request.REQUEST.has_key('u_name') == True:
		if(request.REQUEST['u_name']=='admin' and request.REQUEST['pass']=='chatdb'):
			data=OnlinePresence.objects.all()
			
			for d in data:
				print d.ping_time,time.mktime(datetime.datetime.now().timetuple()) * 1000
				if(abs(d.ping_time-time.mktime(datetime.datetime.now().timetuple())* 1000)>30000):
					d.presence=0
					print d.user_name
					d.save()
	return online_users()