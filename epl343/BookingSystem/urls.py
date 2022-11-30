from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import reverse_lazy
# from django.contrib.auth import views as auth_views

app_name = "bs"

urlpatterns = [
    # No additional argument -> not something at the end of the route
    # What will be displayed is handle by views.index()
    # Name is useful for finding this particural url pattern
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('home/', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contacts, name='contacts'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login1, name='login'),
    path('login-signup/', views.login1, name='login'),
    path('logout/', views.logout1, name='logout1'),
    path('terms/', views.tc, name='tc'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('teaching-experience/', views.teaching, name='teaching'),
    path('gallery/', views.gallery, name='gallery'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('feedback/', views.feedback, name='feedback'),
    path('addTestimonial/', views.addTestimonial, name='addTestimonial'),
    path('makeBooking/',views.makeBooking,name='makeBooking'),
    path('dashboard/myappointments/', views.myappointments, name = 'myappointments'),
    path('dashboard/learningmaterial/', views.learning_material, name = 'learningmaterial'),
    path('makeBooking/requestSubmitted/', views.requestSubmitted, name='requestSubmitted'),
    path('makeBooking/recommend/<str:date>/<str:time>/<str:duration>/', views.BookFromRecommend, name='recommend'),
    path('dashboard/myappointments/<int:week_number>/', views.myappointments, name = 'myappointments'),
    path('changeBooking/<str:startdate>', views.changeBooking, name = 'changeBooking'),
    path('deleteBooking/<str:startdate>/', views.deleteBooking, name = 'deleteBooking'),
    path('request_reset_password/', views.request_reset_password, name='request_reset_password'),
    path('reset_password/<str:token>/', views.reset_password, name='reset_password'),
    path('activate/<str:token>', views.activate, name='email_activation')





] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)