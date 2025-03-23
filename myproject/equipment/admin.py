from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Equipment, EquipmentRequest

# admin can add or remove the equipments, courts or instruments based on their availability
# admin can access the request of the user and can approve or reject the request.
admin.site.register(Equipment)
admin.site.register(EquipmentRequest)