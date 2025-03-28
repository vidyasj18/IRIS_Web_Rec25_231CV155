# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model

# User gets the notification based on the request.
User = get_user_model()

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}: {self.message}'
    
# 
from django.db import models

# class Booking(models.Model):
#     start_time = models.DateTimeField()  # Requires full date & time
#     end_time = models.TimeField()  
#     # Only requires HH:MM:SS

