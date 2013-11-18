import urllib,json
url='http://192.168.7.250:8009/data/messages/'
#http://<ADDRESS>/data/messages/?addMessage=1&send_name=<SENDERS NAME>&recieve_name=<RECIEVERS NAME>&pass=<SENDERS PASSWORD>&content=<MESSAGE CONTENT>
def getMessage(sender,reciever,passw):
    time=None
    query_args = {'send_name':sender,'recieve_name':reciever,'pass':passw}
    data = urllib.urlencode(query_args)
    
    response = urllib.urlopen(url+'?'+'getMessage=1&'+data)
    data = json.loads(response.read())
    
    return data['fields']


def addMessage(sender,reciever,passw,message):
    time=None
    query_args = {'send_name':sender,'recieve_name':reciever,'pass':passw,'content':message}
    data = urllib.urlencode(query_args)
    
    response = urllib.urlopen(url+'?'+'addMessage=1&'+data)
    data = json.loads(response.read())
    
    return data['fields']

def makeTextFile(sender,reciever,passw):
    
print getMessage('Nandan','ishan','nandan')
print '--------------------------------------------------------'
print addMessage('Nandan','ishan','nandan','testing code')
