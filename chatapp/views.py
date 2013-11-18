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
		data=encodeToJson({"auth":authHelper(request.REQUEST['u_name'],request.REQUEST['pass']),"time":tim})
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
		if(authHelper(request.REQUEST['u_name'],request.REQUEST['pass'])):
			d=OnlinePresence.objects.get(user_name=request.REQUEST['u_name'])
			print d.presence,d.user_name,d.ping_time
			d.user_name=request.REQUEST['u_name']
			d.presence=1
			d.ping_time=time.mktime(datetime.datetime.now().timetuple()) * 1000
			d.save()
			
	return online_users()

def online_users():
        # changed here, correct later
	data=SignUp.objects.all()
	
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

# in the url for the getMessage, add 'message'(for recieving message), 'addMessage' for adding new message, 'send_name' for sender id and 'recieve_name' for reciver id
# url for adding messages - 'http://<ADDRESS>/data/messages/?addMessage=1&send_name=<SENDERS NAME>&recieve_name=<RECIEVERS NAME>&pass=<SENDERS PASSWORD>&content=<MESSAGE CONTENT>
def getMessage(request):
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

# url for setting unread - 'http://<ADDRESS>/data/setRead/?setStatus=1&send_name=<SENDERS NAME>&pass=<SENDERS PASSWORD>&message_id=<MESSAGE ID TO BE SET UNREAD>
def setRead(request):
        send_name=request.REQUEST['send_name']
        send_pass=request.REQUEST['pass']
        if request.REQUEST.has_key('setStatus') and (authHelper(send_name,send_pass)==1):
                d=message.objects.filter(id=request.REQUEST['message_id'])
                if(len(d)>0):
                        for msd in d:
                                msd.message_status=1
                                msd.save()
        data=msd.message_status
        return HttpResponse(data, mimetype="application/json")
        
                
        
##def deleteRead():
##        d=message.objects.filter(message_id=1)
##        for message in d:
##                message.delete()
                
def authHelper(u_name,u_pass):
        result = 0
        d=SignUp.objects.filter(user_name=u_name)
        if len(d)>0:
                if d[0].password==u_pass:
                        result = 1
        else:
                result = 2
        return result
                                                                                                        
