from django import forms
from models import SignUp


class SignUpForm(forms.ModelForm):
	
	class Meta:
		##Using Passwrod Widget for passfield
		model = SignUp
		widgets = {
        'password': forms.PasswordInput(), }
		

