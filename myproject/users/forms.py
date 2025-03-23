# contains the `CustomUserCreationForm` to handle
# user registration with additional fields.
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'branch', 'password',)