from django.urls import path
from . import views

app_name = 'equipment'

# all the urls related to equipment will be defined here.
urlpatterns = [
    path('', views.equipment_list, name='equipment_list'),
    path('add/', views.add_equipment, name='add_equipment'),
    path('request/<int:equipment_id>/', views.request_equipment, name='request_equipment'),
]