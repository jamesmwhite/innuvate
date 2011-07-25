from datetime import datetime
from registration.forms import RegistrationForm
from django import forms
from registration.models import RegistrationProfile
from ideas.models import Person
from django.conf import settings 

class InnuvateRegistrationForm(RegistrationForm):

	email = forms.EmailField()

	def clean_email(self):
		emaill = self.cleaned_data['email']
		email_end = settings.EMAIL_END
		if not str(emaill).endswith(email_end):
			raise forms.ValidationError('Email address must end with '+email_end)
		people = Person.objects(email=str(emaill))
		if people and len(people)>0:
			 raise forms.ValidationError('An account with this email address already exists')
		return emaill

	def save(self, profile_callback=None):
		email=self.cleaned_data['email']
		if str(email).endswith('@dnb.com'):
			new_user = RegistrationProfile.objects.create_inactive_user(username=self.cleaned_data['username'],password=self.cleaned_data['password1'],email=self.cleaned_data['email'])
			return new_user
		else:
			new_user = RegistrationProfile.objects.create_inactive_user(username=self.cleaned_data['username'],password=self.cleaned_data['password1'],email=self.cleaned_data['email'])
			return new_user
			#raise forms.ValidationError('Please enter @dnb.com email address')
		
		
		