from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

admin.site.register(CustomUser, UserAdmin)

