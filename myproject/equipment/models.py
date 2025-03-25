from django.db import models
from django.contrib.auth import get_user_model
from notifications.models import Notification

User = get_user_model()

# this class explains the equipment details.
class Equipment(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    availability = models.BooleanField(default=True)
    quantity = models.PositiveIntegerField()
    condition = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# this class explains the equipment request details.
# approved and rejected requests will be notified to the user and it depends on the admin.
class EquipmentRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    duration = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    comment = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.equipment.name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Notification.objects.create(user=self.user, message=f'Your request for {self.equipment.name} is now {self.status}.')
