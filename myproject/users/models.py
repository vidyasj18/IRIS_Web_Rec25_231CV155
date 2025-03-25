from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# defines the `CustomUser` model which extends Django's built-in
# User` model to include `branch` and a unique `email` field.

class CustomUser(AbstractUser):
    branch = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",  # Avoids conflict with auth.User.groups
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions_set",  # Avoids conflict with auth.User.user_permissions
        blank=True
    )


    def __str__(self):
        return self.username
