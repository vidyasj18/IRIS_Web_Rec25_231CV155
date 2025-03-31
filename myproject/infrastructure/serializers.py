""""
serializers :
In Django REST Framework (DRF), serializers are used to convert complex data types such as 
Django model instances into JSON format (which is easy to send via APIs). 
They also handle deserialization, converting JSON data into Django model instances.

For the Infrastructure Booking Module, serializers help in:
1.Converting infrastructure booking data into JSON responses (for API calls).
2. Validating and processing booking requests from students.
3.Ensuring correct data formats and constraints when users interact with the system.
"""

from rest_framework import serializers
from .models import Infrastructure, Booking, WaitlistBooking
from .models import Notification
from datetime import datetime
from django.utils import timezone
from django.db import models

# serializer for handling infrastructure details.
# Used to list available sports facilities.
class InfrastructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Infrastructure
        fields = '__all__'

# serializer for handling booking details.
class BookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # Read-only field to display the student's username
    facility_name = serializers.CharField(source='infrastructure.name',read_only=True)

    class Meta:
        model = Booking
        fields = "__all__"

# Custom validation to ensure:
#   - The student can book only 1 slot per day.
#   - Overlapping bookings are not allowed.
  

    def validate(self, data):
        user = self.context['request'].user
        requested_slot = data.get('requested_slot')
        facility = data.get('facility')
   
    # Ensure the user can book only one slot per day
        if Booking.objects.filter(user=user, requested_slot__date=requested_slot.date(), status="Approved").exists():
            raise serializers.ValidationError("You can only book one slot per day.")

        # Ensure no overlapping bookings
        overlapping_booking = Booking.objects.filter(
            facility=facility,
            requested_slot=requested_slot,
            status="Approved"
        )

        if overlapping_booking.exists():
            raise serializers.ValidationError("This time slot is already booked. Please choose another slot.")

        return data
    
  
    
""""
Serializer for handling waitlist requests
 - Handles students who want to join the waitlist when a slot is already booked.
 - Automatically assigns a position to each waitlisted student.
"""

class WaitlistSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    facility_name = serializers.ReadOnlyField(source='facility.name')

    class Meta:
        model = WaitlistBooking
        fields = '__all__'



# Custom logic:
#  - Add students to the waitlist in sequential order.


    def create(self, validated_data):
        facility = validated_data['facility']
        date = validated_data['date']
        time_slot = validated_data['time_slot']

        # Determine the waitlist position
        position = WaitlistBooking.objects.filter(
            facility=facility, date=date, time_slot=time_slot
        ).count() + 1

        validated_data['position'] = position
        return super().create(validated_data)


# defining a serilizer to convert Notification model instances into JSON format.
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'  

