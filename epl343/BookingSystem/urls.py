from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

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
    path('makeBooking/',views.makeBooking,name='makeBooking'),
    path('dashboard/myappointments/', views.myappointments, name = 'myappointments'),
    # path('dashboard/changeProfile/', views.changeProfile, name = 'changeProfile'),
    path('dashboard/learningmaterial/', views.learning_material, name = 'learningmaterial'),
    path('makeBooking/requestSubmitted/', views.requestSubmitted, name='requestSubmitted'),
    path('makeBooking/recommend/<str:date>/<str:time>/<str:duration>/', views.BookFromRecommend, name='recommend'),
    path('dashboard/myappointments/', views.myappointments, name = 'myappointments'),
<<<<<<< Updated upstream
    path('changeBooking/<str:startdate>', views.changeBooking, name = 'changeBooking'),
    path('deleteBooking/<str:startdate>', views.deleteBooking, name = 'deleteBooking')

    
=======
    path('reset_password/', auth_views.PasswordResetView.as_view(), name = 'reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name = 'password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view, name ='reset_password_confirm'),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
>>>>>>> Stashed changes




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)