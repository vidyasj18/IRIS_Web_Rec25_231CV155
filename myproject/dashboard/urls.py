# defines routes for the student dashboard.

from django.urls import path
from .views import student_dashboard, book_equipment,request_facility, cancel_request
from .views import dashboard_view, dashboard_updates
from .views import waitlistBooking
from . import views  
from .views import custom_admin_dashboard
from .views import update_booking_status


urlpatterns = [
    path('', student_dashboard, name='student_dashboard'),
    path('overview/', dashboard_view, name='dashboard'),
    path('book-equipment/<int:equipment_id>/', book_equipment, name='book_equipment'),
    path('request-facility/<int:facility_id>/', request_facility, name='request_facility'),
    path('cancel-request/<int:request_id>/', cancel_request, name='cancel_request'),
    path("api/dashboard-updates/", dashboard_updates, name="dashboard_updates"),
    path("api/user-bookings/", views.user_bookings, name="user_bookings"),
    path('waitlist-booking/<int:facility_id>/', waitlistBooking, name='waitlist'),
    path('admin-dashboard/', custom_admin_dashboard, name='admin-dashboard'),
    path("update-booking/<int:booking_id>/", update_booking_status, name="update-booking"),
]
