from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model
from .models import *
###################################################
import pdb
#Contact imports
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
#from datetime import date,time

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
class LearningMaterialFormRef(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = LearningMaterialReference
        fields = "__all__"
class FilesLearningMaterialForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = FilesLearningMaterial
        fields = "__all__"
class LearningMaterialForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = LearningMaterial
        fields = "__all__"

class TestimonialForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Testimonial
        fields = ('description',)

class GaleryPhotoForm(forms.ModelForm):

	class Meta:
		model = Photo
		fields =("image","belongs")
class PhotoSectionForm(forms.ModelForm):
	class Meta:
		model = PhotoSection
		fields =("SectionName",)
######################################################
# Create your forms here.
class RegisterForm(forms.ModelForm):
	email = forms.EmailField(required=True)
	password = forms.CharField()
	password1 = forms.CharField()
	first_name = forms.CharField(max_length=255)
	last_name = forms.CharField(max_length=255)
	year = forms.ChoiceField(choices = years.choices)
	
	model = get_user_model()

	def is_valid(self):
		from django.core.exceptions import ValidationError
		valid = super(RegisterForm, self).is_valid()
		try:
			password1 = self.cleaned_data['password']
			password2 = self.cleaned_data['password1']
			if password1!=password2:
				self.add_error('password1', ValidationError('Password and Password Confirmation fields must match.'))
				return False
		except:
			self.add_error('password', ValidationError('Incorrect username or password'))
		return True and valid

	def save(self, commit=True):
		user = super(RegisterForm, self).save(commit=False)
		user.set_password(self.cleaned_data['password'])
		if commit:
			user.save()
		return user

	class Meta:
		model = get_user_model()
		fields = ('email', 'first_name', 'last_name', 'year', 'password')


	


class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)
	first_name = forms.CharField(max_length=255)
	last_name = forms.CharField(max_length=255)
	is_student = forms.BooleanField(required=False)
	preferred_loc = forms.ChoiceField(choices = locations.choices)
	year = forms.ChoiceField(choices = years.choices)
	pay = forms.ChoiceField(choices = payments.choices)


	model = get_user_model()


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
	from django.contrib.auth.forms import ReadOnlyPasswordHashField
	password = ReadOnlyPasswordHashField()
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

class BookingForm(forms.ModelForm):
	date = forms.DateField(required=True,label = "Book Date")
	time = forms.TimeField(required=True,label = "Book Time")
	appointment_duration = forms.IntegerField(required=True,label = "Book Duration")
	start_dateTime = forms.DateTimeField(widget=forms.HiddenInput())
	duration = forms.DurationField(widget=forms.HiddenInput())
	user = forms.ModelChoiceField(queryset=MyUser.objects.all(),widget=forms.HiddenInput())


	class Meta:
		model = Appointment
		fields = ('duration','start_dateTime','user') 

	def is_valid(self):
		valid = super(BookingForm, self).is_valid()
		return valid


	def save(self, commit=True):
		app = super(BookingForm, self).save(commit=False)
		print(self.cleaned_data['duration'])
		print(self.cleaned_data['start_dateTime'])
		if commit:
			app.save()
		return app

class TestimonialForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Testimonial
        fields = ('description',)


class ChangeUserForm(forms.ModelForm):
	email = forms.EmailField(required=True)
	first_name = forms.CharField(max_length=255)
	last_name = forms.CharField(max_length=255)
	year = forms.ChoiceField(choices = years.choices)
	preferred_loc = forms.ChoiceField(choices = locations.choices)
	pay = forms.ChoiceField(choices = payments.choices)
	school = forms.CharField(max_length=255)
	model = get_user_model()

	class Meta:
		model = get_user_model()
		fields = ('first_name', 'last_name', 'year', 'preferred_loc', 'pay', 'school')

	def save(self, commit=True):
		user = MyUser.objects.get(email=self.cleaned_data['email'])
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.year = self.cleaned_data['year']
		user.preferred_loc = self.cleaned_data['preferred_loc']
		user.pay = self.cleaned_data['pay']
		user.school = self.cleaned_data['school']
		user.save()
		return user

