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
   
# status can be either confirmed/rejected/pending confirmation       
def send_booking(status, appointment):
    strong_greeting = "Thank you for your appointment booking"
    status = "\nYour appointment is now " + status
    if( status.contains("pending")):
        status +="from the Admin \n the Admin has been notified and will confirm or reject the appointment as soon as possible"
    
    description = "Update regarding your appointment on " + str(appointment.start_dateTime.date())
    context = {
        'strong_greeting': strong_greeting,
        'paragraph1': description,
        'paragraph2': status
    }
    send(context, "Update regarding your appointment on " + str(appointment.start_dateTime.date()), str(appointment.user.email))


# def send_material_shared_notifications(materialReference):
#     strong_greeting = "Learning Materiak file has been shared with you"
#     description = "File " + 

# def send_reset_password_token()

def send(context, subject, rec_email):
    html_content = render_to_string("email_template.html", context)
    send_mail(
        subject=subject,
        message= html_content,
        html_message=html_content,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[settings.EMAIL_HOST_USER, rec_email]
        )
