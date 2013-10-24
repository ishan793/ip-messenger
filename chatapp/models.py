from django.db import models

# Create your models here.

class SignUp(models.Model):
	user_name = models.CharField("User_Name",max_length=100)
	password = models.CharField("Password",max_length=100)
	def __unicode__ (self):
        	return self.user_name
