from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
# we have used the custom user model
User = get_user_model()

# contains all the information related to equipment while booking.
class Infrastructure(models.Model):
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255) # location of equipment
    capacity = models.IntegerField() # quantity of equipment available
    availability = models.BooleanField(default=True)
    operating_hours = models.CharField(max_length=50)  # e.g., "6 AM - 10 PM"

# Returns the facility name, making it easier to identify instances in the Django admin or shell.
    def __str__(self):
        return self.name

    
# shows the booking details of the user.
class Booking(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    infrastructure = models.ForeignKey(Infrastructure, on_delete=models.CASCADE)
    date = models.DateField() # The date for which booking is requested.
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Cancelled', 'Cancelled')
    ], default='Pending')

    created_at = models.DateTimeField(auto_now_add=True)

# Returns a readable string indicating which user booked which facility and the current status.
    def __str__(self):
        return f"{self.student.username} - {self.infrastructure.name} - {self.date} {self.time_slot}"
    

# This shows details about the waiting list for that particular equipment 
# when the equipment is unavailable, that time user can click on this and be in the waiting list.
# This also shows in what position you are in that waitinglist, once the people ahead of you finish their timeslots user can get the slot.
class Waitlist(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    infrastructure = models.ForeignKey(Infrastructure, on_delete=models.CASCADE)
    date = models.DateField()
    time_slot = models.TimeField()
    position = models.IntegerField() # This show's the users position in that waiting list.

# Returns a descriptive string that shows the waitlist entry.
    def __str__(self):
        return f"Waitlist: {self.student.username} for {self.infrastructure.name} on {self.date} {self.time_slot}"

