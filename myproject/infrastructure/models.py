from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from equipment.models import Equipment

User = get_user_model()

# Model to store sports infrastructure details
class Infrastructure(models.Model):
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255)  # Location of facility
    capacity = models.IntegerField(default=10)  # Maximum number of bookings allowed
    availability = models.BooleanField(default=True)
    operating_hours = models.CharField(max_length=50)  # e.g., "6 AM - 10 PM"

    def __str__(self):
        return self.name

# Booking model to store user reservations
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name="bookings",default=True)
    request_date = models.DateTimeField(auto_now_add=True)
    requested_slot = models.DateTimeField()
    status = models.CharField(
        max_length=20, 
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default='Pending'
    )
    admin_comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.equipment.name} ({self.status})"

# Model for waitlist when facility is fully booked
class WaitlistBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="waitlist_bookings")
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name="waitlists",default=True)
    date = models.DateField()
    time_slot = models.TimeField(default=now)
    position = models.IntegerField()  # User's position in the waitlist

    def __str__(self):
        return f"Waitlist: {self.user.username} for {self.equipment.name} on {self.date} {self.time_slot}"

    class Meta:
        ordering = ['position']  # Ensure waitlist is ordered by position

# Model to store notifications for users
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)  # Track if the notification is read
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message[:50]}"

# Facility request model for users to request bookings
class FacilityRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('waitlisted', 'Waitlisted'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="facility_requests")
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, default=1)  # Replace 1 with a valid facility ID
    time_slot = models.TimeField(default=now)  # Requested booking time
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.username} - {self.equipment.name} ({self.status})"
