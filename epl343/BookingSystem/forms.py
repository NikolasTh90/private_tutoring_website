from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model
from .models import years, payments, locations,Photo,PhotoSection
###################################################
import pdb
#Contact imports
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
######################################################################
#contact source code
class ContactForm(forms.Form):

    name = forms.CharField(max_length=120)
    email = forms.EmailField()
    inquiry = forms.CharField(max_length=120)
    phone = forms.IntegerField()
    message = forms.CharField(widget=forms.Textarea)

    def get_info(self,contactAdmin=False):
        """
        Method that returns formatted information
        :return: subject, msg
        """
        # Cleaned data
        cl_data = super().clean()

        name = cl_data.get('name').strip()
        from_email = cl_data.get('email')
        subject = cl_data.get('inquiry')
        
        msg = f'{name} with email {from_email} said:'
        msg += f'\n"{subject}"\n\n'
        msg += cl_data.get('message')
        if not contactAdmin:
            message = render_to_string("contact_template_user.html",{'name':name,'email':self.cleaned_data['email'],'inquiry':self.cleaned_data['inquiry'],'message':self.cleaned_data['message']})
        else:
            message = render_to_string("contact_template_admin.html",{'name':name,'email':self.cleaned_data['email'],'inquiry':self.cleaned_data['inquiry'],'message':self.cleaned_data['message']})            
        return subject, message

    def send(self):

        subject, msg = self.get_info()
        #ston user
        send_mail(
            subject=subject,
            message=msg,
            html_message=msg,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.RECIPIENT_ADDRESS]#na to ftiakso
        )
        #
        subject, msg = self.get_info(contactAdmin=True)
        send_mail(
            subject=subject,
            message=msg,
            html_message=msg,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.cleaned_data['email']]#na to ftiakso
        )
#########################################################################
#Galery source###########################################
class GaleryPhotoForm(forms.ModelForm):

	class Meta:
		model = Photo
		fields =("image","belongs")
class PhotoSectionForm(forms.ModelForm):
	class Meta:
		model = PhotoSection
		fields =("SectionName",)
######################################################
class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)
	first_name = forms.CharField(max_length=255)
	last_name = forms.CharField(max_length=255)
	is_student = forms.BooleanField(required=False)
	preferred_loc = forms.ChoiceField(choices = locations.choices)
	year = forms.ChoiceField(choices = years.choices)
	pay = forms.ChoiceField(choices = payments.choices)

	model = User = get_user_model()

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.is_student = self.cleaned_data['is_student']
		if user.is_student:
			user.preferred_loc = self.cleaned_data['preferred_loc']
			user.year = self.cleaned_data['year']
			user.pay = self.cleaned_data['pay']
		else:
			user.preferred_loc = payments.choices[4][0]
			user.year = years.choices[8][0]
			user.pay = payments.choices[4][0]
		if commit:
			user.save()
		return user


# Create your forms here.
class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)
	first_name = forms.CharField(max_length=255)
	last_name = forms.CharField(max_length=255)
	is_student = forms.BooleanField(required=False)
	preferred_loc = forms.ChoiceField(choices = locations.choices)
	year = forms.ChoiceField(choices = years.choices)
	pay = forms.ChoiceField(choices = payments.choices)

	model = User = get_user_model()

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.is_student = self.cleaned_data['is_student']
		if user.is_student:
			user.preferred_loc = self.cleaned_data['preferred_loc']
			user.year = self.cleaned_data['year']
			user.pay = self.cleaned_data['pay']
		else:
			user.preferred_loc = payments.choices[4][0]
			user.year = years.choices[8][0]
			user.pay = payments.choices[4][0]
		if commit:
			user.save()
		return user

class LoginForm(forms.ModelForm):
	email = forms.EmailField(required=True)
	password = forms.CharField()



class UserChangeForm(forms.ModelForm):
	"""A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
	password = forms.CharField()
	is_student = forms.BooleanField(required=False)
	preferred_loc = forms.ChoiceField(choices=locations.choices)
	year = forms.ChoiceField(choices=years.choices)
	pay = forms.ChoiceField(choices=payments.choices)

	def is_valid(self):
		from django.core.exceptions import ValidationError
		valid = super(UserChangeForm, self).is_valid()
		loc = self.cleaned_data['preferred_loc']
		year = self.cleaned_data['year']
		pay = self.cleaned_data['pay']
		student = self.cleaned_data['is_student']
		if student == False:
			if year == loc == pay == 'NA':
				return True
			else:
				if year != 'NA':
					self.add_error('year', ValidationError('This user is not a student'))
				if loc != 'NA':
					self.add_error('preferred_loc', ValidationError('This user is not a student'))
				if pay != 'NA':
					self.add_error('pay', ValidationError('This user is not a student'))
				return False
		else:
			if year == 'NA' or loc == 'NA' or pay == 'NA':
				if year == 'NA':
					self.add_error('year', ValidationError('This user is a student'))
				if loc == 'NA':
					self.add_error('preferred_loc', ValidationError('This user is a student'))
				if pay == 'NA':
					self.add_error('pay', ValidationError('This user is a student'))
				return False
		return True

from . import models
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import datetime
from django.forms.widgets import SelectDateWidget
from django.utils import timezone
from .models import MyUser 
# Customer update form
class CustomerUpdateForm(forms.ModelForm):  # update customer details
    first_name = forms.CharField()
    last_name = forms.CharField()
    dob = forms.DateField(widget=SelectDateWidget(years=range(1960, 2022)))
    company_name = forms.CharField()
    company_address = forms.CharField()
    city = forms.CharField()
    country = forms.CharField()
    postcode = forms.IntegerField()
    image = forms.ImageField(widget=forms.FileInput)

    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'dob', 'company_name', 'company_address', 'city', 'country', 'postcode',
                  'image']