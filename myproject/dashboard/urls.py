# defines routes for the student dashboard.

from django.urls import path
from .views import student_dashboard, book_equipment, request_facility, cancel_request

urlpatterns = [
    path('', student_dashboard, name='student_dashboard'),
    path('book-equipment/<int:equipment_id>/', book_equipment, name='book_equipment'),
    path('request-facility/<int:facility_id>/', request_facility, name='request_facility'),
    path('cancel-request/<int:request_id>/', cancel_request, name='cancel_request'),
]
