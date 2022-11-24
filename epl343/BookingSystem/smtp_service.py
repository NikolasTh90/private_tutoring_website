from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


def send_inquiry(form):
    rec_email = form.cleaned_data['email']
    greeting = "Thank you for your inquiry " +form.cleaned_data['name']+" !"
    message = "I received your inquiry. I am trying to answer to your inquiry as soon as possible.\n" + "Inquiry received: \n" + form.cleaned_data['inquiry'] + "\n" + form.cleaned_data['message'] + "\n"+ form.cleaned_data['email'] + "\n" + str(form.cleaned_data['phone'])

    context = {
       'greeting' : greeting,
       'message' : message
    }
    html_content = render_to_string("email_template.html", context)
    send_mail(
        subject=form.cleaned_data['inquiry'],
        message= html_content,
        html_message=html_content,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[settings.EMAIL_HOST_USER, rec_email]
        )
        
def send_booking(status, recipient, appointment):
    context = {
        'status': status,
        'appointment': appointment
    }
    html_content = render_to_string("contact_template_user.html", context)
    send_mail(
        subject=context['inquiry'],
        message= html_content,
        html_message=html_content,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[settings.EMAIL_HOST_USER, recipient]
        )