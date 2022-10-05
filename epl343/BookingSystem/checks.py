from .models import *
import datetime

def is_day_off(requested_date):
    day_offs = DayException.objects.all()  # oi imeres pou eimaste kleistoi
    # simenei oti iparxi ekseresi tin simerini imera
    if (len(day_offs.filter(DayException=requested_date.weekday())) > 0):
        return True
    return False


def argies(month, day):
    argies = DayMonthException.objects.all()  # hmerominies pou einai argies
    if (len(argies.filter(MonthException=month).filter(DayException=day)) > 0):
        return True
    return False


def kleistoi_mines(month):
    kleistoi_mines = MonthException.objects.all()
    if (len((kleistoi_mines.filter(MonthException=month))) > 0):
        return True
    return False

# def daysExceptions(date_time_obj,request=None):
# 	daysExceptions=convertTimeExceptionsToObj(request,0)#en me diarkeia
# 	for x in daysExceptions:
# 		if(date_time_obj.date()>=x[0] and date_time_obj.date()<=x[1]):
# 			return True
# 		return False


def timeExceptions(requested_date):
    timeExceptions = TimeException.objects.all()
    for exceptionDays in timeExceptions:  # EDW PREPEI NA BAZEIS TIS ORES POU THA EISAI KLEISTOS EKEINI TIN IMERA
        if (requested_date.weekday() == exceptionDays.Day and (requested_date.time() >= exceptionDays.StartingTime and requested_date.time() <= exceptionDays.EndingTime)):
            return True
    return False


def orarioHmeras(requested_date, request=None):
    Oraria = Schedule.objects.all()
    for orario in Oraria:
        if requested_date.weekday() == orario.Day and (requested_date.time() >= orario.Opening and requested_date.time() <= orario.Closing):
            return True
    return False


# source=https://stackoverflow.com/questions/10048249/how-do-i-determine-if-current-time-is-within-a-specified-range-using-pythons-da
def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else:  # crosses midnight
        return check_time >= begin_time or check_time <= end_time


def hasCollision(requested_date, duration):
    requestedDayAppointments = Appointment.objects.all()
    

    requested_appoint_starts = requested_date
    requested_appoint_ends = requested_appoint_starts+datetime.timedelta(minutes=duration)
    for other_appointment in requestedDayAppointments:
        if other_appointment.for_date.date() == requested_date.date():
            other_starts = other_appointment.for_date.time
            other_ends = other_starts+datetime.timedelta(minutes=other_appointment.Duration)
            if is_time_between(other_starts, other_ends, requested_appoint_starts) or is_time_between(other_starts, other_ends, requested_appoint_ends):
                return True
    # if(my_appoint_starts.date()!=my_appoint_ends.date()):
    #	booking(my_appoint_ends.date)
    return False
