from django.db import models
from django.contrib.auth import get_user_model
from infrastructure.views import Infrastructure
from equipment.models import Equipment

User = get_user_model()
# Create your models here.
class Facility(models.Model):
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255) # location of equipment
    capacity = models.IntegerField(default=10) # quantity of equipment available
    availability = models.BooleanField(default=True)
    operating_hours = models.CharField(max_length=50)  # e.g., "6 AM - 10 PM"

# Returns the facility name, making it easier to identify instances in the Django admin or shell.
    def __str__(self):
        return self.name
