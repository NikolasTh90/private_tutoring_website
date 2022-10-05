from django.urls import path
from . import views

app_name = "bs"

urlpatterns = [
    # No additional argument -> not something at the end of the route
    # What will be displayed is handle by views.index()
    # Name is useful for finding this particural url pattern
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contacts, name='contacts'),
    path('book/', views.booking, name='booking'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login1, name='login'),
    path('terms/', views.tc, name='tc'),
    path('dashboard/',views.dashboard,name='dashboard'),

]