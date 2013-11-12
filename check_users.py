import urllib
url='http://127.0.0.1:8000/data/flush/'
def ping_server():
	query_args = { 'u_name':'admin', 'pass':'chatdb' }
	data = urllib.urlencode(query_args)
	urllib.urlopen(url+'?'+data)
	
ping_server()