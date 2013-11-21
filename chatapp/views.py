from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render_to_response
from forms import SignUpForm
from django.core.context_processors import csrf
from chatapp.models import *
import json
import datetime,time

def encodeToJson(data):
	'''function that takes an Object and creates a JSON Object from this object'''
	return '{"fields": ' + json.dumps(list(data.values()), cls=DjangoJSONEncoder) + "}"
	
def Authenticate(request):
	'''Function that takes a HTTP request to check whether a user is registered or not and returns a JSON Http response corresponding to whether user name-password combination is right or not'''
	tim=time.mktime(datetime.datetime.now().timetuple()) * 1000
	if request.REQUEST.has_key('u_name') == True:
		if(authHelper(request.REQUEST['u_name'],request.REQUEST['pass'])==1):		
			d=OnlinePresence.objects.get(user_name=request.REQUEST['u_name'])
			print d.presence,d.user_name,d.ping_time
			d.user_name=request.REQUEST['u_name']
			d.presence=1
			d.ping_time=time.mktime(datetime.datetime.now().timetuple()) * 1000
			d.save()		
		data=encodeToJson({"auth":authHelper(request.REQUEST['u_name'],request.REQUEST['pass']),"time":tim})
		return HttpResponse(data, mimetype = "application/json")
		
## Create view for the sign up page.
def register_user(request):
	'''Function to take a HTTP request and returns a SignUp portal to register new users'''
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
	'''Function to save users name to Online Presence tables'''
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

	

def register_success(request):
	'''To be activated when registration is successful takes a request and generates an HTTP response as output'''
	save_to_onpre()
	return render_to_response('register_success.html')

	
	
def online_presence(request):
	'''Function taking a HTTP request as input and  modifies value of request making user to online''' 
	if request.REQUEST.has_key('u_name') == True:
		if(authHelper(request.REQUEST['u_name'],request.REQUEST['pass'])):
			d=OnlinePresence.objects.get(user_name=request.REQUEST['u_name'])
			print d.presence,d.user_name,d.ping_time
			d.user_name=request.REQUEST['u_name']
			d.presence=1
			d.ping_time=time.mktime(datetime.datetime.now().timetuple()) * 1000
			d.save()
			
	return online_users()

def online_users():
    '''Function called from online_presence to return a JSON HTTP response to show which users are online'''   
	data=OnlinePresence.objects.all()
	
	return HttpResponse(encodeToJson(data), mimetype = "application/json")

def flush_all_presence(request):
	'''A function that takes an Http request to keep a check on users which are online and offline a client which has not interacted with the server in the past 30 seconds is modified as offline'''
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

def getMessage(request):
	'''# in the url for the getMessage, add 'message'(for recieving message), 'addMessage' for adding new message, 'send_name' for sender id and 'recieve_name' for reciver id
# url for adding messages - 'http://<ADDRESS>/data/messages/?addMessage=1&send_name=<SENDERS NAME>&recieve_name=<RECIEVERS NAME>&pass=<SENDERS PASSWORD>&content=<MESSAGE CONTENT>
Input - HTTP request and Output-JSON response
'''
        # get senders name and password from url for verification
        send_name=request.REQUEST['send_name']
        send_pass=request.REQUEST['pass']
        # in case query is for getting messages between two individuals
        send_time=datetime.datetime.now()
        if (request.REQUEST.has_key('getMessage') and (authHelper(send_name,send_pass)==1)):
            data=encodeToJson((message.objects.filter(message_recieve=request.REQUEST['recieve_name'])&message.objects.filter(message_send=request.REQUEST['send_name']))
                              |(message.objects.filter(message_recieve=request.REQUEST['send_name'])&message.objects.filter(message_send=request.REQUEST['recieve_name'])))
        # in case query is for adding a new message, status: 0-unread;1-read
        elif request.REQUEST.has_key('addMessage') and (authHelper(send_name,send_pass)==1):
                new_message = message(message_content=request.REQUEST['content'], message_recieve_id=request.REQUEST['recieve_name'],
                                      message_send_id=request.REQUEST['send_name'],message_status=0,message_send_time=send_time,message_recieve_time=send_time)
                new_message.save()
                data=encodeToJson((message.objects.filter(message_recieve=request.REQUEST['recieve_name'])&message.objects.filter(message_send=request.REQUEST['send_name']))
                              |(message.objects.filter(message_recieve=request.REQUEST['send_name'])&message.objects.filter(message_send=request.REQUEST['recieve_name'])))
        # in case wrong user-password combination is send
        elif (authHelper(send_name,send_pass)==0 or authHelper(send_name,send_pass)==2):
                data='Wrong User-password combination'
        else :
                data='inexplicable error'
        return HttpResponse(data, mimetype="application/json")


def setRead(request):
	'''function for setting messages as read - 'http://<ADDRESS>/data/setRead/?setStatus=1&send_name=<SENDERS NAME>&pass=<SENDERS PASSWORD>&message_id=<MESSAGE ID TO BE SET UNREAD>'''
        send_name=request.REQUEST['send_name']
        send_pass=request.REQUEST['pass']
        if request.REQUEST.has_key('setStatus') and (authHelper(send_name,send_pass)==1):
                d=message.objects.filter(id=request.REQUEST['message_id'])
                if(len(d)>0):
                        for msd in d:
                                msd.message_status=1
                                msd.save()
                                data=msd.message_status
        if request.REQUEST.has_key('setRecieveTime') and (authHelper(send_name,send_pass)==1):
			d=message.objects.filter(id=request.REQUEST['message_id'])
			if(len(d)>0):
				for msd in d:
					recieve_time=datetime.datetime.now()
					msd.message_send_time=recieve_time
					msd.save()
					data=str(msd.message_recieve_time)+str(msd.message_send_time)
					
        return HttpResponse(data, mimetype="application/json")
        
def get_Unread(request):
	'''Function to return number of new messages from all other users Input- Http request , Output - JSON response'''
	new_messages=dict()
	if (authHelper(request.REQUEST['u_name'],request.REQUEST['pass'])==1):
		data=message.objects.filter(message_recieve=request.REQUEST['u_name'])
		for d in data:
			if(d.message_status==0):
				if(str(d.message_send) in new_messages):
					new_messages[str(d.message_send)]+=1
				else:
					new_messages[str(d.message_send)]=1
	k=SignUp.objects.all()
	for d in k:
		if d.user_name == request.REQUEST['u_name']:
			continue
		if d.user_name in new_messages:
			continue
		else:
			new_messages[str(d.user_name)]=0
	
	
	print '{"fields": ' + str(json.dumps(new_messages)) + "}"
	return HttpResponse('{"fields": ' + json.dumps(new_messages) + "}", mimetype = "application/json")
                
def authHelper(u_name,u_pass):
	'''Function to match the passed username and password to check whether the given combination is valid or not'''
        result = 0
        d=SignUp.objects.filter(user_name=u_name)
        if len(d)>0:
                if d[0].password==u_pass:
                        result = 1
        else:
                result = 2
        return result
                                                                                                        
## Gives datetime to the client if requested.
def getTime(request):
	'''Function that takes a HTTP request and returns the current server time in seconds'''
	return HttpResponse('{"fields": '+str(time.mktime(datetime.datetime.now().timetuple()))+"}", mimetype = "application/json")
