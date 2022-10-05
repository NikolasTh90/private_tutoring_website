from urllib import request
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.template import loader
from .forms import NewUserForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import MyUser

User = get_user_model()

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({'site' : 'Home'}, request))

def about(request):
    template = loader.get_template('about.html')
    return HttpResponse(template.render({'site' : 'About'}, request))

def contacts(request):
    template = loader.get_template('contacts.html')
    return HttpResponse(template.render({'site' : 'Contacts'}, request))



def booking(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({'site' : 'Booking'}, request))

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
                messages.error(request, 'Invalid Person! You cannot login ')
                return HttpResponseRedirect(reverse('bs:signin'))
        else:
            messages.error(request, 'Invalid Form! Try again ')
            template = loader.get_template('login.html')
            return HttpResponse(template.render({"signinform": AuthenticationForm()}, request))

    else:
        template = loader.get_template('login.html')
        return HttpResponse(template.render(
            {"signinform": AuthenticationForm()}, request))

def tc(request):
    template = loader.get_template('terms.html')
    return HttpResponse(template.render({'site' : 'tc'}, request))

def signup(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created Successfully')
            return HttpResponseRedirect(reverse('bs:signup'))
        else:  # wrong form
            template = loader.get_template('signup.html')
            context = {"signupform": form}
            messages.error(request, 'Invalid form')
            return HttpResponse(template.render(context, request))
    else:  # User accesing for 1st time
        template = loader.get_template('signup.html')
        context = {"signupform": NewUserForm()}
        return HttpResponse(template.render(context, request))

from .forms import CustomerUpdateForm

@login_required(login_url='bs:login')
def dashboard(request):
    client = MyUser.objects.filter(email=request.user.email).first()
    customer_update_form = CustomerUpdateForm(instance=client)
    template =loader.get_template('customer/profile_cust.html')
    context = {
            'customer_update_form': customer_update_form,
            'cust': client,
            'age': 15
        }
    return HttpResponse(template.render(context,request))