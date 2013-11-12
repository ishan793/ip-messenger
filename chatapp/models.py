from django.db import models


# Create your models here.

# This model is reponsible for signup, Roll number should be the primary key.
class SignUp(models.Model):
	user_name = models.CharField("Username", max_length = 100,unique=True)
	email = models.EmailField('Email', max_length = 100)	
	roll_number = models.IntegerField("EnrollemntId", max_length = 10 ,unique=True)
	password = models.CharField("Password", max_length = 100)
	
	
	def __unicode__ (self):
        	return self.user_name
class OnlinePresence(models.Model):
	user_name = models.CharField("Username", max_length = 100,unique=True)
	presence = models.IntegerField("EnrollemntId", max_length = 10)
	ping_time=models.BigIntegerField("Time")
	def __unicode__ (self):
		return self.user_name