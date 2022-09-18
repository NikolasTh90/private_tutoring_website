from urllib import request
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader




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

def login(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({'site' : 'Login'}, request))

def tc(request):
    template = loader.get_template('terms.html')
    return HttpResponse(template.render({'site' : 'tc'}, request))
