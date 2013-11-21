import urllib,json,time
import unicodedata
url='http://192.168.7.250:8000/data/onpre/'

def online_users(uname,passw):
        """This function returns a dictionary obtained from the server. The
        dictionary has all the users as keys and their online/offline status
        as its value. 0 implies that the user is offline and 1 implies that
        the user is online."""
        users_pre=dict()
        query_args = { 'u_name':uname, 'pass':passw }
        data = urllib.urlencode(query_args)
        response = urllib.urlopen(url+'?'+data)
        data = json.loads(response.read())
        for d in data['fields']:
                users_pre[d['user_name']]=d['presence']
        return users_pre

def unread_messages(uname,passw):
        """This function returns a dictionary obtained from the server. The
        dictionary has all the users as keys and the number of unread messages
        from the user as its value."""
        url='http://192.168.7.250:8000/data/getunread/'
        user_unread=dict()
        query_args = { 'u_name':uname, 'pass':passw }
        data = urllib.urlencode(query_args)
        response = urllib.urlopen(url+'?'+data)
        data = json.loads(response.read())
        
        for d in data['fields']:
                tim=unicodedata.normalize('NFKD', d).encode('ascii','ignore')
                user_unread[tim]=data['fields'][d]
        return user_unread
                
        
