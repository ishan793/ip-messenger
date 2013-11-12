import urllib,json,time
url='http://localhost:8000/data/onpre/'

def online_users(uname,passw):
	users_pre=dict()
	query_args = { 'u_name':uname, 'pass':passw }
	data = urllib.urlencode(query_args)
 	response = urllib.urlopen(url+'?'+data)
  	data = json.loads(response.read())
	for d in data['fields']:
		users_pre[d['user_name']]=d['presence']
	return users_pre
print online_users('Mayank','abc')
