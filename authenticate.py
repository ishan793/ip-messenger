
import urllib,json
url='http://127.0.0.1:8000/data/authenticate/'

def authenticate(uname,passw):
	query_args = { 'u_name':uname, 'pass':passw }
	data = urllib.urlencode(query_args)
 	response = urllib.urlopen(url+'?'+data)
  	data = json.loads(response.read())
 	return data['fields'][0]
print authenticate('Nandan','asd')
