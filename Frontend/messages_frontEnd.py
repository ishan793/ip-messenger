import urllib,json,datetime,time
import unicodedata
url='http://192.168.7.250:8000/data/messages/'

###Tets
msg = [{u'message_status': 0, u'message_recieve_time': u'2013-11-18 10:48:20', u'message_send_time': u'2013-11-18 10:48:11', 'message_send_id': 'Nandan', u'message_content': u'testing ', u'message_recieve_id': u'ishan', u'id': 4}, {u'message_status': 0, u'message_recieve_time': u'2013-11-18 10:51:08.064152', u'message_send_time': u'2013-11-18 10:51:08.064152', u'message_send_id': u'Nandan', u'message_content': u'seriously ?', u'message_recieve_id': u'ishan', u'id': 5}, {u'message_status': 0, u'message_recieve_time': u'2013-11-18 10:52:47.625887', u'message_send_time': u'2013-11-18 10:52:47.625887', u'message_send_id': u'Nandan', u'message_content': u'seriously two ?', u'message_recieve_id': u'ishan', u'id': 6}, {u'message_status': 1, u'message_recieve_time': u'2013-11-17 18:40:49.830462', u'message_send_time': u'2013-11-17 18:40:49.830462', u'message_send_id': u'Nandan', u'message_content': u'seriously three ?', u'message_recieve_id': u'ishan', u'id': 7}, {u'message_status': 0, u'message_recieve_time': u'2013-11-18 14:04:44.807993', u'message_send_time': u'2013-11-18 14:04:44.807993', u'message_send_id': u'Nandan', u'message_content': u'testing code', u'message_recieve_id': u'ishan', u'id': 8}, {u'message_status': 0, u'message_recieve_time': u'2013-11-18 17:38:29.325381', u'message_send_time': u'2013-11-18 17:38:29.325381', u'message_send_id': u'Nandan', u'message_content': u'testing code 2', u'message_recieve_id': u'ishan', u'id': 9}, {u'message_status': 0, u'message_recieve_time': u'2013-11-18 17:50:13.672777', u'message_send_time': u'2013-11-18 17:50:13.672777', u'message_send_id': u'Nandan', u'message_content': u'testing code', u'message_recieve_id': u'ishan', u'id': 10}]
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f' 
DATETIME_FORMAT2 = '%Y-%m-%d %H:%M:%S' 

#http://<ADDRESS>/data/messages/?addMessage=1&send_name=<SENDERS NAME>&recieve_name=<RECIEVERS NAME>&pass=<SENDERS PASSWORD>&content=<MESSAGE CONTENT>
def getMessage(sender,reciever,passw):
	'''function to get messages between a sender=receiver pair this function takes senders and receivers user name and receivers password (receiver being the client making request)'''
	time=None
	query_args = {'send_name':sender,'recieve_name':reciever,'pass':passw}
	data = urllib.urlencode(query_args)
    
	response = urllib.urlopen(url+'?'+'getMessage=1&'+data)
	data = json.loads(response.read())
	data['fields'].sort(key=lambda x: x['message_send_time'])
	
	return data['fields']


def addMessage(sender,reciever,passw,message):
	'''function to send a new message takes senders and receivers user name and password as arguments and returns a dictionary with updated message in it'''
	time=None
	query_args = {'send_name':sender,'recieve_name':reciever,'pass':passw,'content':message}
	data = urllib.urlencode(query_args)
	response = urllib.urlopen(url+'?'+'addMessage=1&'+data)
	data = json.loads(response.read())
	data['fields'].sort(key=lambda x: x['message_send_time'])
	return data['fields']



def makeTextFile(sender,reciever,passw, messages):
        '''makes text file given the sender receiver and sets message status as read on the server'''
        text_file = open("messages/"+sender + "_"+ reciever , 'w')
        url_unread='http://192.168.7.250:8000/data/setRead/'
        for message in messages:
                if sender==message['message_recieve_id'] and message['message_status']==0:
                        query_args = {'send_name':sender,'pass':passw,'message_id':message['id']}
                        data = urllib.urlencode(query_args)
                        response = urllib.urlopen(url_unread+'?'+'setStatus=1&'+data)
                        
                tim=calculate_time(message['message_send_time'])
                #print tim
                line = ''
                line += tim + "\t" + message['message_send_id'] + "\t" +\
                                message['message_content']  + '\n'
                text_file.write(line)

        
def calculate_time(object): 
        '''function to return updates on when was the message recieved on the client
		Input is send time of that message by other user and output is the when was the message recieved on this client'''
        url='http://192.168.7.250:8000/data/gettime/'
        response = urllib.urlopen(url) 
        data = json.loads(response.read()) 
        t=int(data['fields']) 
        tim=unicodedata.normalize('NFKD', object).encode('ascii','ignore')
        tim=tim.split('Z')[0]
        tim=tim.split('T')[0]+' '+tim.split('T')[1]
        try: 
                time_sec=time.mktime(datetime.datetime.strptime(tim, DATETIME_FORMAT).timetuple()) 
        except ValueError: 
                time_sec=time.mktime(datetime.datetime.strptime(tim, DATETIME_FORMAT2).timetuple()) 
          
          
        timegap = (t - time_sec - 60*330) 
        #print time_sec, t, time.strftime(DATETIME_FORMAT2, time.localtime(time_sec)),time.strftime(DATETIME_FORMAT2, time.localtime(t-60*330)) 
##        print timegap, str(datetime.datetime.strptime(tim, DATETIME_FORMAT).timetuple()) 
##        print timegap/1000 
        limits = [0,60, 5*60, 70 * 60, 24*60*60] 
##        print limits 
          
        if timegap <= limits[1] and timegap>= limits[0]: 
                return " few seconds ago " 
        elif timegap <= limits[2] and timegap>= limits[1]: 
                return " few minutes ago "
        elif timegap <= limits[3] and timegap >= limits[2]: 
                return " Today, " + str(tim.split(' ')[1].split('.')[0]) 
        else : 
                return tim.split(' ')[0] 
