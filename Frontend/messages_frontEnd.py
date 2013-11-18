import urllib,json
url='http://192.168.7.250:8000/data/messages/'

###Tets
msg = [{u'message_status': 0, u'message_recieve_time': u'2013-11-18 10:48:20', u'message_send_time': u'2013-11-18 10:48:11', 'message_send_id': 'Nandan', u'message_content': u'testing ', u'message_recieve_id': u'ishan', u'id': 4}, {u'message_status': 0, u'message_recieve_time': u'2013-11-18 10:51:08.064152', u'message_send_time': u'2013-11-18 10:51:08.064152', u'message_send_id': u'Nandan', u'message_content': u'seriously ?', u'message_recieve_id': u'ishan', u'id': 5}, {u'message_status': 0, u'message_recieve_time': u'2013-11-18 10:52:47.625887', u'message_send_time': u'2013-11-18 10:52:47.625887', u'message_send_id': u'Nandan', u'message_content': u'seriously two ?', u'message_recieve_id': u'ishan', u'id': 6}, {u'message_status': 1, u'message_recieve_time': u'2013-11-17 18:40:49.830462', u'message_send_time': u'2013-11-17 18:40:49.830462', u'message_send_id': u'Nandan', u'message_content': u'seriously three ?', u'message_recieve_id': u'ishan', u'id': 7}, {u'message_status': 0, u'message_recieve_time': u'2013-11-18 14:04:44.807993', u'message_send_time': u'2013-11-18 14:04:44.807993', u'message_send_id': u'Nandan', u'message_content': u'testing code', u'message_recieve_id': u'ishan', u'id': 8}, {u'message_status': 0, u'message_recieve_time': u'2013-11-18 17:38:29.325381', u'message_send_time': u'2013-11-18 17:38:29.325381', u'message_send_id': u'Nandan', u'message_content': u'testing code 2', u'message_recieve_id': u'ishan', u'id': 9}, {u'message_status': 0, u'message_recieve_time': u'2013-11-18 17:50:13.672777', u'message_send_time': u'2013-11-18 17:50:13.672777', u'message_send_id': u'Nandan', u'message_content': u'testing code', u'message_recieve_id': u'ishan', u'id': 10}]



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

## makes text file given the sender reciever
# TODO: Check if extra getmessage can be removed by passsing messages
def makeTextFile(sender,reciever,passw, messages):
    text_file = open("messages/"+sender + "_"+ reciever , 'w')
    #messages = getMessage(sender,reciever,passw)
    #messages = msg

    # Reading from dict and storing messages
    for message in messages:
        line = ''
        line += message['message_send_id'] + "\t" +\
        message['message_content'] + "\t" +\
        message['message_send_time'].split()[1].split('.')[0] + '\n'
        text_file.write(line)

        
    
    
##print getMessage('Nandan','ishan','nandan')
##print '--------------------------------------------------------'
##print addMessage('Nandan','ishan','nandan','testing code')
##makeTextFile('Nandan', 'ishan', 'nandan')
