from django.urls import path
from . import views

app_name = "bs"

urlpatterns = [
    # No additional argument -> not something at the end of the route
    # What will be displayed is handle by views.index()
    # Name is useful for finding this particural url pattern
    path('', views.index, name='index'),

]