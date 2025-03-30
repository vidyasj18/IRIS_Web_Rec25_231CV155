from django.contrib import admin
from .models import Infrastructure, Booking, WaitlistBooking, Notification, FacilityRequest

admin.site.register(Infrastructure)
admin.site.register(Booking)
admin.site.register(WaitlistBooking)
admin.site.register(Notification)
admin.site.register(FacilityRequest)
