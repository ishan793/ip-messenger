import urllib,json

url='http://192.168.7.250:8000/data/authenticate/'

def authenticate(uname,passw):
        """This function matches the username and the password entered and
        authenticates the user if the password correct by returning 1 and
        returns 0 if the password is wrong. The function also returns 2 if
        the user is not registered in the server database."""
        time=None
        query_args = { 'u_name':uname, 'pass':passw }
        data = urllib.urlencode(query_args)
        response = urllib.urlopen(url+'?'+data)
        data = json.loads(response.read())
        if(data['fields'][0]==1):
                time=data['fields'][1]
                
        return data['fields'][0]

