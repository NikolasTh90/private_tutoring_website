from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


def send_inquiry(form):
    rec_email = form.cleaned_data['email']
    strong_greeting = "Thank you."
    greeting = "Thank you for your inquiry " +form.cleaned_data['name']+" !"
    message = "I received your inquiry. I am trying to answer to your inquiry as soon as possible.\n" + "Inquiry received: \n" + form.cleaned_data['inquiry'] + "\n" + form.cleaned_data['message'] + "\n"+ form.cleaned_data['email'] + "\n" + str(form.cleaned_data['phone'])

    context = {
        'strong_greeting': strong_greeting,
       'paragraph1' : greeting,
       'paragraph2' : message
    }
    send(context, form.cleaned_data['inquiry'], rec_email)
   
# status can be either confirmed/rejected/pending      
def send_booking(status, appointment):
    strong_greeting = "Thank you for your appointment booking"
    status = "\nYour appointment is now " + status
    if( "pending" in status):
        status +=" confirmation from the Admin! \n the Admin has been notified and will confirm or reject the appointment as soon as possible"
    if( "rejected" in status):
        status +=" by the Admin! \n Please try to book an appointment again for a different date or time, since the Admin might be busy the time you requested"
    if ( "confirmed" in status):
        status +=" by the Admin! \n Looking forward for our appointment!"
    description = "Update regarding your appointment on " + str(appointment.start_dateTime.date()) + " at " + str(appointment.end_dateTime.time())
    context = {
        'strong_greeting': strong_greeting,
        'paragraph1': description,
        'paragraph2': status
    }
    send(context, "Update regarding your appointment on " + str(appointment.start_dateTime.date()), str(appointment.user.email))


def send_material_shared_notifications(materialReference):
    strong_greeting = "Learning Material file has been shared with you"
    description = "File " + materialReference.LearningMaterial.name + " has been shared and you can view it in your dashboard!"
    view_materials_link = "You can see it here: https://www.drsteliostheodorou.com/dashboard/learningmaterial"
    context = {
        'strong_greeting': strong_greeting,
        'paragraph1': description,
        'paragraph2': view_materials_link
    }
    send(context, "New learning material file shared with you", str(materialReference.User.email))

def send_reset_password_token(token, email):
    strong_greeting = "Password Reset request"
    description = "Copy the token to it's field at www.drsteliostheodorou.com/reset_password"
    token = str(token)
    context = {
        'strong_greeting': strong_greeting,
        'paragraph1': description,
        'paragraph2': token
    }
    send(context, "Reset Password at Dr Stelios Theodorou", str(email))

def send_activation_token(token, email):
    strong_greeting = "Account activation required"
    description = "Visit this link to activate your account: www.drsteliostheodorou.com/activate/"+token
    token = str(token)
    context = {
        'strong_greeting': strong_greeting,
        'paragraph1': description,
        'paragraph2': ""
    }
    send(context, "Account activation at Dr Stelios Theodorou", str(email))


def send(context, subject, rec_email):
    html_content = render_to_string("email_template.html", context)
    send_mail(
        subject=subject,
        message= html_content,
        html_message=html_content,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[settings.EMAIL_HOST_USER, rec_email]
        )
