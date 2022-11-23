from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

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
    path('booking/', views.booking, name='booking'),
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
    path('learningmaterial/', views.addLearningMaterial, name='addlearningmaterial'),
    path('addfiletolearningmaterial/', views.addFileToMaterial, name='learningmaterialasas'),
    path('userViewMaterial/', views.userViewMaterial, name='userViewMaterialsda'),
    path('viewmaterial/<int:id>', views.viewmaterial, name='viewmateriall'),
    path('addAllLearningMaterial/<int:id>', views.addUserToLearningMaterial, name='addUserToLearningMateriald'),
    path('getalllearningmaterialadmin/', views.getAllLearningMaterial, name='getallmaterial'),
    path('addTestimonial/', views.addTestimonial, name='addTestimonial'),
    path('temp/',views.temp,name='temp'),
    path('myappointments/', views.myappointments, name = 'myappointments')




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)