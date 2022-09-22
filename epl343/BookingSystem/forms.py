from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model



# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)
	first_name = forms.CharField(max_length=255)
	last_name = forms.CharField(max_length=255)

	model = User = get_user_model()

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		if commit:
			user.save()
		return user