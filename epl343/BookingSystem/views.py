from .forms import CustomerUpdateForm,ContactForm
from urllib import request
from .forms import LoginForm, RegisterForm,BookingForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.template import loader
from .forms import NewUserForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model, logout, login
from django.contrib.auth.decorators import login_required
from .models import *
from .BookingSystem import main

import datetime


User = get_user_model()


def index(request):
    template = loader.get_template('index.html')
    testimonials = Testimonial.objects.all().values()
    auth = False
    name = None
    if request.user.is_authenticated:
        auth = True
        name = request.user.first_name

    return HttpResponse(template.render({'site': 'Home', 'testimonials': testimonials, 'authenticated' : auth, 'name' : name}, request))

def temp(request) :
    if (request.method == "POST") :
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
        template =loader.get_template('signup.html')
        return HttpResponse(template.render({}, request))

    else :
        template = loader.get_template('signup.html')
        return HttpResponse(template.render({'form': BookingForm() }, request))

def myappointments(request):
    appointments = Appointment.objects.filter(user = MyUser.objects.get(email = 'epl343@ucy.ac.cy'))
    list_app = []
    for a in range(len(appointments)):
        print(type(appointments[a].start_dateTime))
        list_app.append(appointments[a].start_dateTime)
        print(appointments[a].start_dateTime)
    min = list_app[0]
    for appoint in range(len(appointments)):
        if list_app[appoint]<min :
            min=list_app[appoint]
    print(min)
    max = list_app[0]
    for appoint in range(len(appointments)):
        if list_app[appoint]>max :
            max=list_app[appoint]
    print(max)
    template = loader.get_template('appointments_schedule/index.html')
    return HttpResponse(template.render({'app' : appointments}, request))

def about(request):
    template = loader.get_template('about.html')
    return HttpResponse(template.render({'site': 'About'}, request))


def contacts(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			form.send()
			messages.success(request, ('Your message was sent!'))
		else:
			messages.error(request, ('Please correct the error below.'))
	template = loader.get_template('contacts.html')
	return HttpResponse(template.render({'site': 'Contacts'}, request))

def booking(request):
    template = loader.get_template('booking.html')
    post_request={'requested_dateTime': datetime.datetime(2022,11,30,16),
                'requested_duration': datetime.timedelta(minutes = 60),
                'user_email': 'nikolasth90@gmail.com',
                'description': 'i need help!',
                'location': 'Online'

                }
    main(post_request)
    return HttpResponse(template.render({'site': 'Booking'}, request))    

def teaching(request):
    # template = loader.get_template('teaching_experience.html')
    experiences = Teaching_experience.objects.all().order_by('-start_date').values()
    return render(request, "teaching_experience.html", {'site': 'TeachingExperience', 'experiences': experiences} )

def feedback(request):
    return render(request, "feedback.html", {'site': 'Feedback'})

def testimonials(request):
    # template = loader.get_template('teaching_experience.html')
    testimonials = Testimonial.objects.all().values()
    return render(request, "testimonials.html", {'site': 'Testimonials', 'testimonials': testimonials} )

def logout1(request):
    logout(request)
    return HttpResponseRedirect(reverse('bs:index'))

def login1(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('bs:dashboard'))
        
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('bs:dashboard'))
        else:
            messages.error(request, 'Invalid username or password.')
            template = loader.get_template('login.html')
            return HttpResponse(template.render({"signinform": AuthenticationForm(), 'login' : True}, request))

    else:
        template = loader.get_template('login.html')
        return HttpResponse(template.render(
            {"login" : True, 'site': 'Login'}, request))


def tc(request):
    template = loader.get_template('terms.html')
    return HttpResponse(template.render({'site': 'tc'}, request))


def signup(request):
    context = {"login": False, 'site' : 'Login'}
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('bs:login'))
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            authenticate(request, username=user.email, password=user.password)
            login(request, user)
            messages.success(request, 'Account created Successfully')
            return HttpResponseRedirect(reverse('bs:login'))
        else:  # wrong form
            template = loader.get_template('login.html')
            for error in form.errors:
                if str(error)=='email':
                    messages.error(request, 'A user with this email already exists.')
                if error=='password':
                    print(error)
                    messages.error(request, 'Wrong Username or password.')
                if error=='password1':
                    messages.error(request, 'Password and confirmation must be the same.')
            return HttpResponseRedirect(reverse('bs:login'))
    else:  # User accesing for 1st time
        return HttpResponseRedirect(reverse('bs:login'))


@login_required(login_url='bs:login')
def dashboard(request):
    client = MyUser.objects.filter(email=request.user.email).first()
    customer_update_form = CustomerUpdateForm(instance=client)
    template = loader.get_template('customer/profile_cust.html')
    context = {
            'customer_update_form': customer_update_form,
            'cust': client,
            'age': 15
        }
    return HttpResponse(template.render(context, request))

##########################################################################################################################
######################################################################################
#Galery code
# def viewPhotoSections(request):
# 	sections=PhotoSection.objects.all()
# 	context = {'sections': sections}
# 	return render(request, 'applicationForReg/ticket_system.html', context)
# def viewPhotoBasedOnSection(request,section):
# 	photos=Photo.objects.all().filter(belongs=section)
# 	context = {'photos': photos}
# 	return render(request, 'applicationForReg/ticket_system.html', context)
# def uploadPhoto(request):
# 	if request.user.is_superuser:
# 		if  request.method == 'POST':
# 			form=GaleryPhotoForm(request.POST)#
# 			if(form.is_valid()):
# 				messages.success(request, _('Your photo was posted!'))
# 				form.save()
# 			else:
# 				messages.error(request, _('kati pai X.'))#
# 		else:
# 			form=GaleryPhotoForm()
# 			context = {'form': form}
# 			return form
# def addSection(request):
# 	if request.user.is_superuser:
# 		if  request.method == 'POST':
# 			form=PhotoSectionForm(request.POST)
# 			if(form.is_valid()):
# 				messages.success(request, _('Your Section was posted!'))
# 				form.save()
# 			else:
# 				messages.error(request, _('kati pai X.'))#
# 		else:
# 				form=PhotoSectionForm()
# 				context = {'form': form}
# 				return form
######################################################################################
