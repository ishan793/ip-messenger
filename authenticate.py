
import urllib,json
url='http://127.0.0.1:8000/data/authenticate/'

def authenticate(uname,passw):
	time=None
	query_args = { 'u_name':uname, 'pass':passw }
	data = urllib.urlencode(query_args)
 	response = urllib.urlopen(url+'?'+data)
  	data = json.loads(response.read())
	if(data['fields'][0]==1):
		time=data['fields'][1]
 	return data['fields'][0],time

print authenticate(a,'abc')
