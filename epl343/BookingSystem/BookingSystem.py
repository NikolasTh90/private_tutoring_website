import datetime
from .models import Schedule, Offs, Appointment, MyUser
from django.db.models import Q
import django.utils.timezone as timezone
from .smtp_service import send_booking
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
        #end email notification
        send_booking("pending")

    else:
        recommendations = [recommend_next_appointment(post_request['requested_dateTime'], post_request['requested_duration']),
                            recommend_previous_appointment(post_request['requested_dateTime'], post_request['requested_duration'])] 
        return recommendations  

def Available(requested_dateTime, requested_duration, current_appointment=None):
		if not is_valid_appointment_request(requested_dateTime):
			return False

		if appointment_is_available(requested_dateTime, requested_duration, current_appointment):
			return True
			#create appointment model
			#user = MyUser.objects.only(email).filter(email=post_request['user_email'])
			#TODO user should be a MyUser instance, can we get this from sessions?
			Appointment.objects.create(user = post_request['user_email'], description = post_request['description'], duration = requested_duration, start_dateTime = requested_dateTime) 
			#TODO send email notification
		else:
			return False

def makeRecommendations(requested_dateTime, requested_duration):
		return [recommend_previous_appointment(requested_dateTime, requested_duration),
                    recommend_next_appointment(requested_dateTime, requested_duration)] 

def is_valid_appointment_request(requested_appointment_dateTime):
    now = datetime.datetime.now()
    current_datetime = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=now.hour, minute=now.minute, second=now.second, tzinfo=timezone.utc) + allowed_days_before_appointment
    if requested_appointment_dateTime < current_datetime:
        return False
    return True    



def appointment_is_available(requested_appointment_start_dateTime, requested_appointment_duration, current_appointment):
    if is_compatible_with_schedule(requested_appointment_start_dateTime, requested_appointment_duration) and not is_in_offs(requested_appointment_start_dateTime, requested_appointment_duration) and not is_colliding_with_appointment(requested_appointment_start_dateTime, requested_appointment_duration, current_appointment) and has_break_between_appointments(requested_appointment_start_dateTime):
        return True
    return False

def has_break_between_appointments(requested_appointment_start_dateTime):
    appointments = Appointment.objects.all()
    has_appointments_on_request_dateTime = False
    for app in appointments:
        if app.start_dateTime.date() == requested_appointment_start_dateTime.date():
            has_appointments_on_request_dateTime = True
            if not (app.end_dateTime).time() <= (requested_appointment_start_dateTime - break_time).time():
                return False
    if not has_appointments_on_request_dateTime:
        return True
    return True


def returnMax(requested_dateTime, duration, end_of_day):
    if requested_dateTime.date() != (requested_dateTime + duration).date():
        return end_of_day
    return requested_dateTime + duration

def is_compatible_with_schedule(requested_appointment_start_dateTime, requested_duration):
    requested_weekday = requested_appointment_start_dateTime.weekday()
    weekday_schedule = Schedule.objects.all().filter(Day=requested_weekday)
    end_of_day = datetime.datetime(1,1,1,23,59)
    for schedule_entry in weekday_schedule:
        if requested_appointment_start_dateTime.time() >= schedule_entry.Opening and returnMax(requested_appointment_start_dateTime, requested_duration, end_of_day).time() <= schedule_entry.Closing :
            return True
    return False    

def is_in_offs(requested_appointment_start_dateTime, requested_appointment_duration):
    offs = Offs.objects.all()
    for off in offs:
        if requested_appointment_start_dateTime + requested_appointment_duration >= off.start_dateTime.replace(tzinfo=timezone.utc) and requested_appointment_start_dateTime  <= off.end_dateTime.replace(tzinfo=timezone.utc):
            return True
    return False        

def is_colliding_with_appointment(requested_appointment_start_dateTime, requested_appointment_duration, current_appointment):
    other_appointments = Appointment.objects.all().filter( start_dateTime__date = requested_appointment_start_dateTime.date() ).filter(Q(pending = True) | Q(accepted = True) )
    for other in other_appointments:
        if other is None or other == current_appointment:
            if requested_appointment_start_dateTime + requested_appointment_duration >= other.start_dateTime.replace(tzinfo=timezone.utc) and requested_appointment_start_dateTime <= other.end_dateTime.replace(tzinfo=timezone.utc):
                return True

    return False 

def recommend_next_appointment(requested_appointment_start_dateTime, requested_appointment_duration):
    recommend_next_appointment_datetime = requested_appointment_start_dateTime
    recommend_next_appointment_datetime += datetime.timedelta(minutes=5)
    while True:
        if Available(recommend_next_appointment_datetime, requested_appointment_duration, current_appointment=None):
            return recommend_next_appointment_datetime
        recommend_next_appointment_datetime += datetime.timedelta(minutes=5)
    

def recommend_previous_appointment(requested_appointment_start_dateTime, requested_appointment_duration):
    recommended_previous_appointment_dateTime = requested_appointment_start_dateTime - datetime.timedelta(minutes=5)
    now = datetime.datetime.now()
    current_datetime = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=now.hour, minute=now.minute, second=now.second, tzinfo=timezone.utc) + allowed_days_before_appointment
    while recommended_previous_appointment_dateTime >= current_datetime:
        if Available(recommended_previous_appointment_dateTime, requested_appointment_duration, current_appointment=None):
            return recommended_previous_appointment_dateTime
        recommended_previous_appointment_dateTime -= datetime.timedelta(minutes=5)
    
    return None       

