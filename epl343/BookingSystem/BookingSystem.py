<<<<<<< HEAD
import datetime
from .models import Schedule, Offs, Appointment, MyUser
from django.db.models import Q
break_time = datetime.timedelta(minutes = 10)
allowed_days_before_appointment = datetime.timedelta(days = 3)

def main(post_request):
    if not is_valid_appointment_request(post_request['requested_dateTime']):
        return Exception("Invalid date")

    if appointment_is_available(post_request['requested_dateTime'], post_request['requested_duration']):
        #create appointment model
        #user = MyUser.objects.only(email).filter(email=post_request['user_email'])
        #TODO user should be a MyUser instance, can we get this from sessions?
        Appointment.objects.create(user = post_request['user_email'], description = post_request['description'], duration = post_request['requested_duration'], start_dateTime = post_request['requested_dateTime']) 
        #TODO send email notification

    else:
        recommendations = [recommend_next_appointment(post_request['requested_dateTime'], post_request['requested_duration']),
                            recommend_previous_appointment(post_request['requested_dateTime'], post_request['requested_duration'])] 
        return recommendations  


def is_valid_appointment_request(requested_appointment_dateTime):
    if requested_appointment_dateTime < datetime.datetime.now() + allowed_days_before_appointment:
        return False
    return True    



def appointment_is_available(requested_appointment_start_dateTime, requested_appointment_duration):
    if is_compatible_with_schedule(requested_appointment_start_dateTime, requested_appointment_duration) and not is_in_offs(requested_appointment_start_dateTime, requested_appointment_duration) and not is_colliding_with_appointment(requested_appointment_start_dateTime, requested_appointment_duration):
        return True
    
    return False

def is_compatible_with_schedule(requested_appointment_start_dateTime, requested_duration):
    requested_weekday = requested_appointment_start_dateTime.weekday()
    weekday_schedule = Schedule.objects.all().filter(Day=requested_weekday)
    for schedule_entry in weekday_schedule:
        if requested_appointment_start_dateTime.time() >= schedule_entry.Opening and (requested_appointment_start_dateTime + requested_duration).time() <= schedule_entry.Closing :
            return True

    return False    

def is_in_offs(requested_appointment_start_dateTime, requested_appointment_duration):
    offs = Offs.objects.all()
    for off in offs:
        if requested_appointment_start_dateTime + requested_appointment_duration >= off.start_dateTime.replace(tzinfo=None) and requested_appointment_start_dateTime  <= off.end_dateTime.replace(tzinfo=None):
            return True
    
    return False        

def is_colliding_with_appointment(requested_appointment_start_dateTime, requested_appointment_duration):
    other_appointments = Appointment.objects.all().filter( start_dateTime__date = requested_appointment_start_dateTime.date() ).filter(Q(pending = True) | Q(accepted = True) )
    for other in other_appointments:
        if requested_appointment_start_dateTime + requested_appointment_duration >= other.start_dateTime.replace(tzinfo=None) and requested_appointment_start_dateTime <= other.end_dateTime.replace(tzinfo=None):
            return True

    return False 

def recommend_next_appointment(requested_appointment_start_dateTime, requested_appointment_duration):
    recommended_next_appointment = requested_appointment_start_dateTime + datetime.timedelta(minutes=5)
    while True:
        if appointment_is_available(recommended_next_appointment, requested_appointment_duration):
            return recommended_next_appointment
        recommended_next_appointment = requested_appointment_start_dateTime + datetime.timedelta(minutes=5)
    

def recommend_previous_appointment(requested_appointment_start_dateTime, requested_appointment_duration):
    recommended_previous_appointment = requested_appointment_start_dateTime - datetime.timedelta(minutes=5)
    while recommended_previous_appointment >= datetime.datetime.now() + allowed_days_before_appointment:
        if appointment_is_available(recommended_previous_appointment, requested_appointment_duration):
            return recommended_previous_appointment
        recommended_previous_appointment = requested_appointment_start_dateTime - datetime.timedelta(minutes=5)
    
    return None       

=======
import datetime
from .models import Schedule, Offs, Appointment, MyUser
from django.db.models import Q
break_time = datetime.timedelta(minutes = 10)
allowed_days_before_appointment = datetime.timedelta(days = 3)
# post_request={requested_dateTime: datetime.datetime(2022,11,30,16),
#                 requested_duration: datetime.timedelta(minutes = 60),
#                 user_email: 'nikolasth90@gmail.com',
#                 description: 'i need help!',
#                 location: 'Online',

#                 }




def main(post_request):
    if not is_valid_appointment_request(post_request['requested_dateTime']):
        return Exception("Invalid date")

    if appointment_is_available(post_request['requested_dateTime'], post_request['requested_duration']):
        #create appointment model
        #user = MyUser.objects.only(email).filter(email=post_request['user_email'])
        #TODO user should be a MyUser instance, can we get this from sessions?
        Appointment.objects.create(user = post_request['user_email'], description = post_request['description'], duration = post_request['requested_duration'], start_dateTime = post_request['requested_dateTime']) 
        #TODO send email notification

    else:
        recommendations = [recommend_next_appointment(post_request['requested_dateTime'], post_request['requested_duration']),
                            recommend_previous_appointment(post_request['requested_dateTime'], post_request['requested_duration'])] 
        return recommendations  


def is_valid_appointment_request(requested_appointment_dateTime):
    if requested_appointment_dateTime < datetime.datetime.now() + allowed_days_before_appointment:
        return False
    return True    



def appointment_is_available(requested_appointment_start_dateTime, requested_appointment_duration):
    if is_compatible_with_schedule(requested_appointment_start_dateTime, requested_appointment_duration) and not is_in_offs(requested_appointment_start_dateTime, requested_appointment_duration) and not is_colliding_with_appointment(requested_appointment_start_dateTime, requested_appointment_duration):
        return True
    
    return False

def is_compatible_with_schedule(requested_appointment_start_dateTime, requested_duration):
    requested_weekday = requested_appointment_start_dateTime.weekday()
    weekday_schedule = Schedule.objects.all().filter(Day=requested_weekday)
    for schedule_entry in weekday_schedule:
        if requested_appointment_start_dateTime.time() >= schedule_entry.Opening and (requested_appointment_start_dateTime + requested_duration).time() <= schedule_entry.Closing :
            return True

    return False    

def is_in_offs(requested_appointment_start_dateTime, requested_appointment_duration):
    offs = Offs.objects.all()
    for off in offs:
        if requested_appointment_start_dateTime + requested_appointment_duration >= off.start_dateTime.replace(tzinfo=None) and requested_appointment_start_dateTime  <= off.end_dateTime.replace(tzinfo=None):
            return True
    
    return False        

def is_colliding_with_appointment(requested_appointment_start_dateTime, requested_appointment_duration):
    other_appointments = Appointment.objects.all().filter( start_dateTime__date = requested_appointment_start_dateTime.date() ).filter(Q(pending = True) | Q(accepted = True) )
    for other in other_appointments:
        if requested_appointment_start_dateTime + requested_appointment_duration >= other.start_dateTime.replace(tzinfo=None) and requested_appointment_start_dateTime <= other.end_dateTime.replace(tzinfo=None):
            return True

    return False 

def recommend_next_appointment(requested_appointment_start_dateTime, requested_appointment_duration):
    recommended_next_appointment = requested_appointment_start_dateTime + datetime.timedelta(minutes=5)
    while True:
        if appointment_is_available(recommended_next_appointment, requested_appointment_duration):
            return recommended_next_appointment

def recommend_previous_appointment(requested_appointment_start_dateTime, requested_appointment_duration):
    recommended_previous_appointment = requested_appointment_start_dateTime - datetime.timedelta(minutes=5)
    while recommended_previous_appointment >= datetime.datetime.now() + allowed_days_before_appointment:
        if appointment_is_available(recommended_previous_appointment, requested_appointment_duration):
            return recommended_previous_appointment
    return False       

>>>>>>> 54e850644a3b9425c4538760e279d2165bd09632
