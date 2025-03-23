from django.urls import path
from . import views

app_name = 'notifications'

# all the urls related to notifications will be defined here.
urlpatterns = [
    path('', views.notifications_list, name='notifications_list'),
]