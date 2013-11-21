from django.db import models
from django.db.models.fields.related import ManyToManyField, ForeignKey


# Create your models here.

# This model is reponsible for signup, Roll number should be the primary key.
class SignUp(models.Model):
        """The model describes the sql table representing user"""
	user_name = models.CharField("Username", max_length = 100,unique=True, primary_key=True)
	email = models.EmailField("Email", max_length = 100)	
	roll_number = models.IntegerField("EnrollemntId", max_length = 10 ,unique=True)
	password = models.CharField("Password", max_length = 100)
	
	
	def __unicode__ (self):
        	return self.user_name
class OnlinePresence(models.Model):
        """The model describes the sql table for online users"""
	user_name = models.CharField("Username", max_length = 100,unique=True)
	presence = models.IntegerField("EnrollemntId", max_length = 10)
	ping_time=models.BigIntegerField("Time")
	def __unicode__ (self):
		return self.user_name

# 
class message(models.Model):
        """Class representing the table for a message"""
	message_content = models.CharField('Content', max_length = 100)
	message_status = models.IntegerField('Status', max_length = 1)	
	message_send=ForeignKey(SignUp,related_name='Sender+')
        message_recieve=ForeignKey(SignUp,related_name='Reciever+')
        
        message_send_time=models.DateTimeField()
        message_recieve_time=models.DateTimeField()
    
        def __unicode__(self):  # Python 3: def __str__(self):
                return self.message_content
