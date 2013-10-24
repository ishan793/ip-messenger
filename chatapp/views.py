from django.http import HttpResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

from chatapp.models import *

import json

def encodeToJson(data):
	return '{"fields": ' + json.dumps(list(data.values()), cls=DjangoJSONEncoder) + "}"
	
def Authenticate(request):
	if request.REQUEST.has_key('u_name') == True:
		if(SignUp.objects.filter(user_name=request.REQUEST['u_name']) and SignUp.objects.filter(password=request.REQUEST['pass'])):
			data=encodeToJson({"auth":1})
			
			return HttpResponse(data, mimetype = "application/json")
		else:
			data=encodeToJson({"auth":0})			
			return HttpResponse(data, mimetype = "application/json")
