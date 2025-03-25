from django.urls import path
from . import views

app_name = 'equipment'

# all the urls related to equipment will be defined here.
urlpatterns = [
    path('', views.equipment_list, name='equipment_list'),
    path('add/', views.add_equipment, name='add_equipment'),
    path('request/', views.request_equipment, name='request_equipment'),
    path('approve/<int:request_id>/', views.approve_request, name='approve_request'),
    path('reject/<int:request_id>/', views.reject_request, name='reject_request'),
]