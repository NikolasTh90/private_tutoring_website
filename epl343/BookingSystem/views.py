from .forms import CustomerUpdateForm,ContactForm
from urllib import request
from .forms import LoginForm, RegisterForm
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
from .checks import *

import datetime


User = get_user_model()


def index(request):
    template = loader.get_template('index.html')
    testimonials = Testimonial.objects.all().values()

    return HttpResponse(template.render({'site': 'Home', 'testimonials': testimonials}, request))


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
            messages.error(request, 'Please try again')
            template = loader.get_template('login.html')
            return HttpResponse(template.render({"signinform": AuthenticationForm()}, request))

    else:
        template = loader.get_template('login.html')
        return HttpResponse(template.render(
            {"signinform": AuthenticationForm()}, request))


def tc(request):
    template = loader.get_template('terms.html')
    return HttpResponse(template.render({'site': 'tc'}, request))


def signup(request):
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
            context = {}
            messages.error(request, 'Invalid form')
            messages.error(request, form.errors)
            return HttpResponse(template.render(context, request))
    else:  # User accesing for 1st time
        template = loader.get_template('login.html')
        context = {"signupform": NewUserForm()}
        return HttpResponse(template.render(context, request))


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
# def booking(request, findNextBest=True, target_date=None):
#     template = loader.get_template('index.html')
#     if request.method == 'POST':
#         if findNextBest:
#             requested_date = datetime.datetime.strptime(request.POST['theDate'], '%Y-%m-%dT%H:%M')  # convert the date to datetime object

#         else:
# 			# requested_date = datetime.datetime.strptime(specific_date_time_string, '%Y-%m-%dT%H:%M')#convert the date to datetime object
#             requested_date = target_date
# 		#########################################################################################################################
#         if (is_day_off(requested_date)):  # simenei oti iparxi ekseresi tin simerini imera
#             if not findNextBest:
#                 return False
#             messages.error(request, _('Pote den dulevume tetoies imeres.'))

#         if (argies(requested_date.month, requested_date.day)):
#             if not findNextBest:
#                 return False
#             messages.error(request, _('Tin sigekrimeni imera eimaste kleistoi panta.'))

#         if (kleistoi_mines(requested_date.month)):
#             if not findNextBest:
#                 return False
#         messages.error(request, _('Ton sigekrimeno mina eimaste kleistoi.'))

#         # if (daysExceptions(requested_date, request)):
#         #     if not findNextBest:
#         #         return False
#         #     messages.error(request, _('eimaste kleistoi tin sigkekrimeni periodo.'))

#         if (timeExceptions(requested_date, request)):
#             if not findNextBest:
#                 return False
#             messages.error(request, _('kleinume pio grigora aftin tin imera.'))
#         if (not orarioHmeras(requested_date, request)):
#             if not findNextBest:
#                 return False
#         messages.error(request, _(
# 			    'simfona me to orario mas aftin tin imera imaste klistoi.'))

#         if (hasCollision(requested_date, 60)):
#             if not findNextBest:
#                 return False
#             messages.error(request, _('iparxi alo rantevou.'))

#         # hasColission(2022, requested_date.month, requested_date.day,
# 		#              requested_date, 60, request)


#     # else:
#     #     form = AppointmentForm()
#     #     return render(request, 'applicationForReg/book.html', {'form': form})




#     return HttpResponse(template.render({'site' : 'Booking'}, request))
