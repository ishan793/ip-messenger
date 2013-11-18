##def authenticate(u,p):
##    flag=0
##    if u=='Raj Shah' and p=='b':
##        flag=1
##    return flag
    

import urllib,json
url='http://192.168.7.250:8000/data/authenticate/'

def authenticate(uname,passw):
        time=None
        query_args = { 'u_name':uname, 'pass':passw }
        data = urllib.urlencode(query_args)
        response = urllib.urlopen(url+'?'+data)
        data = json.loads(response.read())
        if(data['fields'][0]==1):
                time=data['fields'][1]
        return data['fields'][0]
