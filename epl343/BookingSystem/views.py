from .forms import CustomerUpdateForm,ContactForm
from urllib import request
from .forms import *
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model, logout, login
from django.contrib.auth.decorators import login_required
from .models import *
from django.utils.timezone import timedelta
from .BookingSystem import *
import numpy as np
from . import smtp_service
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.core.files.storage import FileSystemStorage
from django.conf import settings

User = get_user_model()

def addTestimonial(request):
    """
    form=None
    if(len(Appointment.objects.all().filter(user=request.user))!=0):
        form=TestimonialForm()
    if request.method == 'POST':
        usersapp=Appointment.objects.all().filter(user=request.user).filter(accepted=True)#.filter(end_dateTime<datetime.now())
        #if(len(userapp)>0):
        #Den itan etimo to adminpanel giana kanw accepted,to fevgete apo comment
        flag=False
        Testimonial.objects.all().filter(user=request.user).delete()
        model=Testimonial(user=request.user,description=request.POST['description'])
        model.save()
    """

    # Get the current timestamp
    timestampNow=datetime.datetime.now()

    # The number of total accepted appointments of the user that have ended
    noOfUserAppointments = len(Appointment.objects.all().filter(user=request.user).filter(accepted=True).filter(end_dateTime__lt=timestampNow))

    # Get existing testimonial (if it exists)
    try:
        existingTestimonial = Testimonial.objects.get(user=request.user)
    except ObjectDoesNotExist:
        existingTestimonial = None

    # If request is POST, check if the user already has a testimonial.
    # If a testimonial exists, update the existing testimonial
    # Else, create a new testimonial
    if request.method == 'POST':
        if existingTestimonial:
            existingTestimonial.description = request.POST['description']
            existingTestimonial.save()
        else:
            model = Testimonial(user=request.user, description=request.POST['description'])
            model.save()
    appointments = Appointment.objects.filter(user = request.user)
    first_week_with_appointments = 0
    if len(appointments) >= 1:
        first_week_with_appointments = appointments[0].start_dateTime.isocalendar().week
    # IF request is GET, ...

    return render(request, "customer/add_testimonial.html", {'Site': 'AddTestimonial', 'NoOfUserAppointments': noOfUserAppointments, 'CallBackMethod': request.method, 'ExistingTestimonial': existingTestimonial, 'first_week_with_appointments' : first_week_with_appointments} )
    
def index(request):
    template = loader.get_template('index.html')
    testimonials = Testimonial.objects.all()

    return HttpResponse(template.render({'site': 'Home', 'testimonials': testimonials}, request))

def deleteBooking(request,startdate):
    if request.user.is_authenticated:
        
        start_date = datetime.datetime(year=int(startdate[:4]),month=int(startdate[5:7]),day=int(startdate[8:10]), hour=int(startdate[11:13]), minute=int(startdate[13:15]), second=0)
        print(start_date)

        app = Appointment.objects.filter(start_dateTime=start_date).first()
        where_to_redirect = str(app.start_dateTime.isocalendar().week)
        if app.user == request.user:
            app.delete()
    return HttpResponseRedirect('/dashboard/myappointments/' + where_to_redirect)
        

def changeBooking(request,startdate):
    if request.user.is_authenticated:
        if (request.method == "POST"):
            start_date = datetime.datetime(year=int(startdate[:4]),month=int(startdate[5:7]),day=int(startdate[8:10]), hour=int(startdate[11:13]), minute=int(startdate[13:15]), second=0)
            date = request.POST.get('date')
            time = request.POST.get('time')
            duration = request.POST.get('appointment_duration')
            requested_dateTime = datetime.datetime(year=int(date[:4]),month=int(date[5:7]),day=int(date[8:]), hour=int(time[:2]), minute=int(time[3:5]), second=0, tzinfo=timezone.utc)
            requested_duration = timedelta(hours=int(duration)//60, minutes=int(duration)%60)
            if Available(requested_dateTime=requested_dateTime, requested_duration=requested_duration, current_appointment=Appointment.objects.filter(start_dateTime=start_date).first()):
                current_appointment = Appointment.objects.get(start_dateTime=start_date)
                same_date_flag = True
                if current_appointment.start_dateTime != requested_dateTime:
                    same_date_flag = False
                    current_appointment.start_dateTime = requested_dateTime
                current_appointment.duration = requested_duration
                current_appointment.description = request.POST.get('description')
                current_appointment.location = request.POST.get('location')
                if not same_date_flag:
                    current_appointment.pending = True
                    current_appointment.accepted = False
                    current_appointment.save()
                    Appointment.objects.filter(start_dateTime=start_date).delete()
                else:
                    current_appointment.save()
                return HttpResponseRedirect(reverse('bs:requestSubmitted'))
            else:
                requested_dateTime, requested_duration = strToDateTime(date, time, duration)
                recommendations = np.array(makeRecommendations(requested_dateTime=requested_dateTime, requested_duration=requested_duration))
                recommendations = recommendations[np.where(recommendations!=None)]
                request.session['recommended'] = True
                request.session['location']=request.POST.get('location')
                request.session['description']=request.POST.get('description')
                final_recommendations = list()
                for recommend in recommendations:
                    temp = [recommend, str(recommend.date()), str(recommend.time()), duration]
                    final_recommendations.append(temp)
                template = loader.get_template('appointments_schedule/changebooking.html')    
                return HttpResponse(template.render({'recommendations' : final_recommendations, 'recommend' : True, 'site' : 'Booking'}, request))
        else:
            template = loader.get_template('appointments_schedule/changebooking.html')
            start_date = datetime.datetime(year=int(startdate[:4]),month=int(startdate[5:7]),day=int(startdate[8:10]), hour=int(startdate[11:13]), minute=int(startdate[13:15]), second=0)
            current_appointment = Appointment.objects.filter(start_dateTime=start_date).first()
            duration = str(current_appointment.duration)
            duration = int(duration[:1])*60 + int(duration[2:4])
            location = current_appointment.location
            description = current_appointment.description
            return HttpResponse(template.render({'form' : BookingForm, 'previous_date' : startdate[:10], 'previous_time' : (startdate[11:13] + ':' + startdate[13:15]), 'previous_location' : location, 'previous_description' : description, 'previous_duration' : duration}, request))
        

def strToDateTime(date, time, duration):
    requested_dateTime = datetime.datetime(year=int(date[:4]),month=int(date[5:7]),day=int(date[8:]), hour=int(time[:2]), minute=int(time[3:5]), second=0, tzinfo=timezone.utc)
    requested_duration = timedelta(hours=int(duration)//60, minutes=int(duration)%60)
    return requested_dateTime, requested_duration

def updateRequestWith(request_copy, requested_dateTime, requested_duration, user, date, time, duration, location, description):
    request_copy.update({'start_dateTime' : requested_dateTime })
    request_copy.update({'duration' :   requested_duration })
    if user is not None:
        request_copy.update({'user' : user })
        request_copy.update({'date' :   date })
        request_copy.update({'time' :   time })
        request_copy.update({'appointment_duration' :   duration })
        request_copy.update({'location' :   location })
        request_copy.update({'description' :   description })
    return request_copy

def makeBooking(request):
    try:        
        if request.session['waitforlogin'] == True:    
            date = request.session['date']
            time = request.session['time']
            print(date)
            duration = request.session['duration']
            location = request.session['location']
            print('hd', date)
            print(time)
            #pay = request.session['pay']
            description = request.session['description']
            user = request.user
            requested_dateTime, requested_duration = strToDateTime(request.session['date'], request.session['time'], request.session['duration'])
            request_copy = request.POST.copy()
            request_copy = updateRequestWith(request_copy, requested_dateTime, requested_duration, user, date, time, duration, location, description)
            form = BookingForm(data = request_copy)
            form.start_dateTime = requested_dateTime
            form.duration = requested_duration
            form.user = user
            form.location = location
            #form.pay = pay
            form.description = description
            request.session['waitforlogin'] = False
            if Available(requested_dateTime=requested_dateTime, requested_duration=requested_duration):
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect(reverse('bs:requestSubmitted'))
            else:
                template = loader.get_template('bookingform/makebooking.html')
                requested_dateTime, requested_duration = strToDateTime(date, time, duration)
                recommendations = np.array(makeRecommendations(requested_dateTime=requested_dateTime, requested_duration=requested_duration))
                recommendations = recommendations[np.where(recommendations!=None)]
                request.session['recommended'] = True
                request.session['location'] = request.POST.get('location')
                request.session['description'] = request.POST.get('description')
                final_recommendations = list()
                for recommend in recommendations:
                    temp = [recommend, str(recommend.date()), str(recommend.time()), duration]
                    final_recommendations.append(temp)
                return HttpResponse(template.render({'recommendations' : final_recommendations, 'recommend' : True, 'site' : 'Booking'}, request))
        else:
            if (request.method == "POST") :
                request_copy = request.POST.copy()
                date = request.POST.get('date')
                time = request.POST.get('time')
                duration = request.POST.get('appointment_duration')
                requested_dateTime, requested_duration = strToDateTime(date, time, duration)
                request_copy = updateRequestWith(request_copy, requested_dateTime, requested_duration, None, None, None, None, None, None)
                form = BookingForm(data = request_copy)
                if Available(requested_dateTime=requested_dateTime, requested_duration=requested_duration):
                    if request.user.is_authenticated:
                        request_copy.update({'user' : request.user  })
                        form = BookingForm(data = request_copy)
                        if form.is_valid():
                            form.save()
                        return HttpResponseRedirect(reverse('bs:requestSubmitted'))
                    else:
                        # Prepare session to redirect to login
                        request.session['date'] = date
                        request.session['time'] = time
                        request.session['duration'] = duration
                        request.session['location'] = request.POST.get('location')
                        request.session['description'] = request.POST.get('description')
                        #request.session['pay'] = request.POST.get('pay')
                        request.session['waitforlogin'] = True
                        return HttpResponseRedirect('/login-signup/?next=/makeBooking/')
                else:
                    template = loader.get_template('bookingform/makebooking.html')
                    requested_dateTime, requested_duration = strToDateTime(date, time, duration)
                    recommendations = np.array(makeRecommendations(requested_dateTime=requested_dateTime, requested_duration=requested_duration))
                    recommendations = recommendations[np.where(recommendations!=None)]
                    request.session['recommended'] = True
                    request.session['description'] = request.POST.get('description')
                    request.session['location'] = request.POST.get('location')
                    a = recommendations[0]
                    final_recommendations = list()
                    for recommend in recommendations:
                        temp = [recommend, str(recommend.date()), str(recommend.time()), duration]
                        final_recommendations.append(temp)
                    return HttpResponse(template.render({'recommendations' : final_recommendations, 'recommend' : True, 'site' : 'Booking'}, request))
            else :
                template = loader.get_template('bookingform/makebooking.html')
                return HttpResponse(template.render({'recommend' : False, 'site' : 'Booking'}, request))
    except:
        if (request.method == "POST") :
                request_copy = request.POST.copy()
                date = request.POST.get('date')
                time = request.POST.get('time')
                duration = request.POST.get('appointment_duration')
                requested_dateTime, requested_duration = strToDateTime(date, time, duration)
                request_copy = updateRequestWith(request_copy, requested_dateTime, requested_duration, None, None, None, None, None, None)
                form = BookingForm(data = request_copy)
                if Available(requested_dateTime=requested_dateTime, requested_duration=requested_duration):
                    if request.user.is_authenticated:
                        request_copy.update({'user' : request.user  })
                        form = BookingForm(data = request_copy)
                        if form.is_valid():
                            form.save()
                        return HttpResponseRedirect(reverse('bs:requestSubmitted'))
                    else:
                        # Prepare session to redirect to login
                        request.session['date'] = date
                        request.session['time'] = time
                        request.session['duration'] = duration
                        request.session['location'] = request.POST.get('location')
                        request.session['description'] = request.POST.get('description')
                        #request.session['pay'] = request.POST.get('pay')
                        request.session['waitforlogin'] = True
                        return HttpResponseRedirect('/login-signup/?next=/makeBooking/')
                else:
                    template = loader.get_template('bookingform/makebooking.html')
                    requested_dateTime, requested_duration = strToDateTime(date, time, duration)
                    recommendations = np.array(makeRecommendations(requested_dateTime=requested_dateTime, requested_duration=requested_duration))
                    recommendations = recommendations[np.where(recommendations!=None)]
                    request.session['recommended'] = True
                    request.session['description'] = request.POST.get('description')
                    request.session['location'] = request.POST.get('location')
                    a = recommendations[0]
                    final_recommendations = list()
                    for recommend in recommendations:
                        temp = [recommend, str(recommend.date()), str(recommend.time()), duration]
                        final_recommendations.append(temp)
                    return HttpResponse(template.render({'recommendations' : final_recommendations, 'recommend' : True, 'site' : 'Booking'}, request))
        else :
            template = loader.get_template('bookingform/makebooking.html')
            return HttpResponse(template.render({'recommend' : False, 'site' : 'Booking'}, request))


    

def requestSubmitted(request):
    template = loader.get_template('BookingRequestSubmitted.html')
    return HttpResponse(template.render({}, request))

def BookFromRecommend(request, date, time, duration):
    print('gdhfsdjkhfkdsjhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
    try:
        print('gdhfsdjkhfkdsjhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
        if request.session['recommended']==True:
            if request.user.is_authenticated:
                print('gdhfsdjkhfkdsjhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
                requested_dateTime, requested_duration = strToDateTime(date, time, duration)
                if Available(requested_dateTime=requested_dateTime, requested_duration=requested_duration):
                    print('gdhfsdjkhfkdsjhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
                    Appointment.objects.create(user = request.user, description = request.session['description'], duration = requested_duration, start_dateTime = requested_dateTime, location=request.session['location']) 
                    request.session['recommended'] = False
                    return HttpResponseRedirect(reverse('bs:requestSubmitted'))
            else:
                return HttpResponseRedirect('/login-signup/?next=/makeBooking/recommend/' + date + '/' + time + '/' + duration + '/')

        else:
            return HttpResponseRedirect(reverse('bs:makeBooking'))    
    except:
        return HttpResponseRedirect(reverse('bs:makeBooking'))


def myappointments(request, week_number):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('bs:login'))
    temp_appointments = Appointment.objects.filter(user = request.user)
    appointments = list()
    weeks_with_apps = list()
    for app in temp_appointments:
        if app.start_dateTime.isocalendar().week not in weeks_with_apps:
            weeks_with_apps.append(app.start_dateTime.isocalendar().week)
        if app.start_dateTime.isocalendar().week == week_number:
            appointments.append(app)
    weeks_with_apps.sort()
    if len(appointments) >= 1:
        dt = datetime.datetime.strptime(appointments[0].start_dateTime.date().strftime("%d/%m/%Y"), '%d/%m/%Y')
        start = dt - timedelta(days=dt.weekday())
        end = start + timedelta(days=6)
        print(start)
        print(end)
        first_week_with_appointments = appointments[0].start_dateTime.isocalendar().week
    else:
        first_week_with_appointments = list()
    try:
        minstart = appointments[0].start_dateTime.time()
        maxend = appointments[0].end_dateTime.time()
        for app in appointments:
            if app.start_dateTime.time() < minstart:
                minstart = app.start_dateTime.time()
            if app.end_dateTime.time() > maxend:
                maxend = app.end_dateTime.time()
        delta = datetime.timedelta(minutes=60)
        maxend = (datetime.datetime.combine(datetime.date(1,1,1),maxend) + delta).time()
        print(minstart, maxend)

        dict = {0 : 'Monday', 1 : 'Tuesday', 2 : 'Wednesday', 3 : 'Thursday', 4 : 'Friday', 5 : 'Saturday', 6 : 'Sunday'}
        appointments_sorted_by_weekday = list()
        for i in range(5):
            weekday_apps = [dict[i]]
            counter = 1
            for app in appointments:
                print(app)
                if app.start_dateTime.weekday()==i:
                    weekday_apps.append([app, counter])
                    counter += 1
                    if counter == 5:
                        counter = 1
            appointments_sorted_by_weekday.append(weekday_apps)
        print(appointments_sorted_by_weekday)
        slots = []
        counter = 0
        midnight = datetime.datetime(year=1, month=1, day=1, hour=23, minute=59)
        # for dynamic start time use:
        #  minstart = datetime.datetime.combine(date=datetime.date(1,1,1),time=minstart)
        
        # for static start time use:
        minstart = datetime.datetime.combine(date=datetime.date(1,1,1),time=datetime.time(8,0,0))


        while (minstart.time()<maxend or counter < 30) and minstart.date()==midnight.date():
            slots.append(minstart.time())
            delta = datetime.timedelta(minutes=30)
            print(minstart, delta, minstart + delta)
            minstart = minstart + delta
            counter += 1
        print(slots)
        template = loader.get_template('appointments_schedule/index.html')
        return HttpResponse(template.render({'appointments_sorted' : appointments_sorted_by_weekday,'slot': slots, 'week_num' : week_number, 'weeks' : weeks_with_apps, 'week_start' : start, 'week_end' : end, 'first_week_with_appointments' : first_week_with_appointments, 'cust' : request.user}, request))
    except:
        template = loader.get_template('appointments_schedule/index.html')
        dict = {0 : 'Monday', 1 : 'Tuesday', 2 : 'Wednesday', 3 : 'Thursday', 4 : 'Friday', 5 : 'Saturday', 6 : 'Sunday'}
        appointments_sorted_by_weekday = list()
        for i in range(5):
            weekday_apps = [dict[i]]
            appointments_sorted_by_weekday.append(weekday_apps)
        print(week_number)
        return HttpResponse(template.render({'appointments_sorted' : appointments_sorted_by_weekday, 'week_num' : week_number, 'weeks' : weeks_with_apps, 'first_week_with_appointments' : first_week_with_appointments, 'cust' : request.user}, request))

def about(request):
    template = loader.get_template('about.html')
    return HttpResponse(template.render({'site': 'About'}, request))


def contacts(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			smtp_service.send_inquiry(form)
			messages.success(request, ('Your message was sent!'))
		else:
			messages.error(request, ('Please correct the error below.'))
	template = loader.get_template('contacts.html')
	return HttpResponse(template.render({'site': 'Contacts'}, request))

def teaching(request):
    # template = loader.get_template('teaching_experience.html')
    experiences = Teaching_experience.objects.filter(show=True).order_by('-start_date')
    return render(request, "teaching_experience.html", {'site': 'TeachingExperience', 'experiences': experiences} )

def feedback(request):
    return render(request, "feedback.html", {'site': 'Feedback'})

def testimonials(request):
    # template = loader.get_template('teaching_experience.html')
    testimonials = Testimonial.objects.select_related('user')
    return render(request, "testimonials.html", {'site': 'Testimonials', 'testimonials': testimonials} )

def gallery(request):
    sections = PhotoSection.objects.all().order_by('SectionName')
    photos = Photo.objects.all()
    return render(request, "gallery.html", {'site': 'Gallery', 'sections': sections, 'photos': photos})

def logout1(request):
    logout(request)
    return HttpResponseRedirect(reverse('bs:index'))

def request_reset_password(request):
    if request.method == "POST":
        newrequest = ({
            'User' : MyUser.objects.filter(email=request.POST.get('email')).first(),
            'email' : request.POST.get('email'),
        })
        form = RequestResetPassword(data = newrequest)
        if len(ResetTokens.objects.filter(User=MyUser.objects.get(email=request.POST.get('email')))) != 0:
            ResetTokens.objects.filter(User=MyUser.objects.get(email=request.POST.get('email'))).delete()
        if form.is_valid():
            form.save()
            template = loader.get_template('request_reset_password.html')
            return HttpResponse(template.render({'mess' : 'If the user exists, you will find an email with a reset password link in your email', 'sent' : True}, request))
        else:
            print(form.errors)
            template = loader.get_template('request_reset_password.html')
            return HttpResponse(template.render({'sent' : False},request)) 
    else:
        template = loader.get_template('request_reset_password.html')
        return HttpResponse(template.render({'sent' : False},request))    

def reset_password(request, token):
    if ResetTokens.objects.filter(Token=token).first() is not None:
        if request.method == "POST":
            newrequest = ({
                'email' : ResetTokens.objects.filter(Token=token).first().User,
                'password' : request.POST.get('password'),
                'password1' : request.POST.get('password1')
            })
            form = ResetPassword(newrequest)
            if form.is_valid():
                template = loader.get_template('reset_password.html')
                return HttpResponse(template.render({'valid' : True, 'post' : True, 'Finished' : 'Password Successfully changed'},request))
            else :
                print(form.errors)
                
        else:
            template = loader.get_template('reset_password.html')
            return HttpResponse(template.render({'valid' : True, 'post' : False},request))      
    else:
        template = loader.get_template('reset_password.html')
        return HttpResponse(template.render({'mess' : 'Link is invalid', 'valid' : False, 'post' : False},request))     
        


def login1(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('bs:dashboard'))
        
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = MyUser.objects.get(email=email)
            if user is not None:                
                user = authenticate(request, username=email, password=password)
                login(request, user)    
                if str(request.GET.get('next')).__contains__('/makeBooking/'):
                    return HttpResponseRedirect(request.GET.get('next'))
                return HttpResponseRedirect(reverse('bs:dashboard'))    
        else:
            try:
                email = form.cleaned_data['username']
                user = MyUser.objects.get(email=email)
                # If user exists in the database but is not active, print according message
                if user is not None:
                    if not user.is_active:
                        messages.error(request, 'Please verify your email to login. We have sent you an email with instructions.')
                        activationToken = ActivateTokens.objects.get(User=user.id).Token
                        smtp_service.send_activation_token(activationToken, user.email)
                        template = loader.get_template('login.html')
                        return HttpResponse(template.render({"signinform": AuthenticationForm(), 'login' : True}, request))
            # If user does not exist in the database, again print according message
            except ObjectDoesNotExist: 
                messages.error(request, 'Invalid username or password.')
                template = loader.get_template('login.html')
                return HttpResponse(template.render({"signinform": AuthenticationForm(), 'login' : True}, request))
    # If not a post request 
    else:
        # Check for account activation status
        if request.session.get('activationStatus') == 'activated':
            messages.success(request, 'Your account has been activated successfully.')
        
        if request.session.get('activationStatus') == 'error':
            messages.success(request, 'Invalid activation link.')
        request.session["activationStatus"] = ""
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
            activationRecord = ActivateTokens(User=user)
            activationToken = activationRecord.generate_token()
            messages.success(request, 'Account created Successfully. Please verify your account. An email has been sent to your email address.')
            smtp_service.send_activation_token(activationToken, user.email)
            return HttpResponseRedirect(reverse('bs:login'))
        else:  # wrong form
            template = loader.get_template('login.html')
            for error in form.errors:
                if str(error)=='email':
                    messages.error(request, 'A user with this email already exists.')
                if error=='password':
                    messages.error(request, 'Wrong Username or password.')
                if error=='password1':
                    messages.error(request, 'Password and confirmation must be the same.')
            return HttpResponseRedirect(reverse('bs:login'))
    else:  # User accesing for 1st time
        return HttpResponseRedirect(reverse('bs:login'))


@login_required(login_url='bs:login')
def dashboard(request):
    if (request.method == "POST") :
        form = ChangeUserForm(request.POST)
        print(request.POST.get('first_name'))
        print(request.POST.get('last_name'))
        print(request.POST.get('year'))
        print(request.POST.get('email'))
        if request.POST.get('profilepic') != '':
            myfile = request.FILES['profilepic']
        if form.is_valid():
            if request.POST.get('profilepic') != '':
                fs = FileSystemStorage(location= settings.MEDIA_ROOT + '/images/ProfilePics/')
                myfile.name = myfile.name
                filename = fs.save(myfile.name, myfile)
                uploaded_file_url = 'images/ProfilePics/' + myfile.name
                user = MyUser.objects.get(email=request.user.email)
                if 'DefaultProfilePic.png' not in user.profilePic.file.name:
                    os.remove(user.profilePic.file.name)
                user.profilePic.name = uploaded_file_url
                user.save()
            form.save()
        else:
            print(form.errors)
            print("Your change form is not correct")
        
    
        return HttpResponseRedirect(reverse('bs:dashboard'))
    else :
        client = MyUser.objects.filter(email=request.user.email).first()
        customer_update_form = CustomerUpdateForm(instance=client)
        template = loader.get_template('customer/profile_cust.html')

        appointments = Appointment.objects.filter(user = client)
        first_week_with_appointments = 0
        if len(appointments) >= 1:
            first_week_with_appointments = appointments[0].start_dateTime.isocalendar().week
        context = {
                'customer_update_form': customer_update_form,
                'cust': client,
                'first_week_with_appointments' : first_week_with_appointments
            }
        return HttpResponse(template.render(context, request))

@login_required(login_url='bs:login')
def learning_material(request):
    client = MyUser.objects.filter(email=request.user.email).first()
    customer_update_form = CustomerUpdateForm(instance=client)
    template = loader.get_template('customer/view_learning_material.html')
    materials_reference=LearningMaterialReference.objects.all().filter(User__id=request.user.id).values('LearningMaterial')
    materials = []
    for reference in materials_reference:
        materials.append(LearningMaterial.objects.get(id=reference['LearningMaterial']))
    supported_icons = ["aac","avi","bmp","dll","doc","eps","flv","gif","html","iso","jpg","midi","mov","mp3","mpg","pdf","png","ppt","psd","tif","txt","wmv","xls","zip"]
    appointments = Appointment.objects.filter(user = client)
    first_week_with_appointments = 0
    if len(appointments) >= 1:
        first_week_with_appointments = appointments[0].start_dateTime.isocalendar().week
    context = {
            'cust': client,
            'materials': materials,
            'supported_icons': supported_icons,
            'first_week_with_appointments' : first_week_with_appointments
        }

    return HttpResponse(template.render(context, request))


def activate(request, token):

    activateTokenRecord = ActivateTokens.objects.filter(Token=token).first()
    
    if activateTokenRecord is not None:
        print(activateTokenRecord.Token)
        print(activateTokenRecord.User)
        userRecord = MyUser.objects.get(id=activateTokenRecord.User.id)
        userRecord.is_active = True
        userRecord.save()
        request.session["activationStatus"] = "activated"
        return HttpResponseRedirect(reverse('bs:login'))

    request.session["activationStatus"] = "error"
    return HttpResponseRedirect(reverse('bs:login'))



# def addLearningMaterial(request):
#     if request.user.is_authenticated and request.user.is_staff:
#         if request.method == "GET":#epistrefis forma
#             return render(request, "addlearningmaterial.html", {'materialform': LearningMaterialForm()})
#         if request.method == "POST":
#             learning_material=LearningMaterialForm(request.POST)#kanis tin forma construct
#             if(learning_material.is_valid()):#an einai valid
#                 learning_material.save()#apothikevse tin
#                 message="succeed"
#             else:#alios epestrepse error
#                 message="error"
#             return render(request, "addlearningmaterial.html", {'materialform': LearningMaterialForm(),'message':message})
# def getAllLearningMaterial(request):
#     if request.user.is_authenticated and request.user.is_staff:
#         allmaterial=LearningMaterial.objects.all()
#         return render(request, "getalllearningmaterial.html", {'allmaterials': allmaterial})
# def addUserToLearningMaterial(request,id):
#     if request.user.is_authenticated and request.user.is_staff:
#         if request.method == "GET":#epistrefis forma
#             usersall=MyUser.objects.all()#epestrepse olus tus xristes
#             return render(request, "addusertomaterial.html", {'usersall': usersall})
#         if request.method == "POST":#epistrefis forma
#             usersall=MyUser.objects.all()
#             material=LearningMaterial.objects.filter(pk=id)
#             LearningMaterialReference.objects.all().filter(LearningMaterial__id=id).delete()
#             for x in usersall:
#                 if(str(x.id) in request.POST):
#                     LearningMaterialReference(User=x,LearningMaterial=material[0]).save()
#             return render(request, "addusertomaterial.html", {'usersall': usersall,'FilesLearningMaterialForm':FilesLearningMaterialForm()})
# def addFileToMaterial(request):
#     if request.user.is_authenticated and request.user.is_staff:
#         if request.method == "GET":#epistrefis forma
#             return render(request, "addfiletomaterial.html", {'FilesLearningMaterialForm':FilesLearningMaterialForm()})
#         if request.method == "POST":#epistrefis forma
#             form=FilesLearningMaterialForm(request.POST,request.FILES)
#             msg=None
#             if form.is_valid():
#                 msg="succeed"
#                 form.save()
#             else:
#                 msg="failed"
#             return render(request, "addfiletomaterial.html", {'FilesLearningMaterialForm':FilesLearningMaterialForm(),'message':msg})
# def userViewMaterial(request):
#     if request.user.is_authenticated:
#         learningmat=LearningMaterialReference.objects.filter(User__id=request.user.id)
#         return render(request, "viewlearningmaterial.html", {'learningmat':learningmat})
# def viewmaterial(request,id):
#     learningmat=FilesLearningMaterial.objects.filter(LearningMaterialFK__id=id)#vrisko to antikimeno
#     if(len(learningmat)!=0):
#         learningMaterialMainObject=learningmat[0].LearningMaterialFK#dixnw ston dixti tou learningmaterial antikimenou
#         references=LearningMaterialReference.objects.all().filter(LearningMaterial=learningMaterialMainObject).filter(User=request.user)#vrisko an iparxi erotima gia afton ton xristi
#         if(len(references)==0):#an to material den iparxi ston xristi den tha tou emfaniso kati
#             learningmat=None
#     else:#den iparxun arxia
#         message="no files"
#     return render(request, "viewmaterialfiles.html", {'learningmat':learningmat})




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
