from django.contrib import admin
from .models import Infrastructure, Booking, Waitlist

# Register your models here.
# admin can make changes or has rights to change all the models given below.
admin.site.register(Infrastructure)
admin.site.register(Booking)
admin.site.register(Waitlist)