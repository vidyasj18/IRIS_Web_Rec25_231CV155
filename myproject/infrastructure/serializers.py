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
from .models import Infrastructure, Booking, Waitlist
from .models import Notification

# serializer for handling infrastructure details.
# Used to list available sports facilities.
class InfrastructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Infrastructure
        fields = '__all__'

# serializer for handling booking details.
class BookingSerializer(serializers.ModelSerializer):
    student = serializers.ReadOnlyField(source='student.username')  # Read-only field to display the student's username
    infrastructure_name = serializers.ReadOnlyField(source='infrastructure.name')

    class Meta:
        model = Booking
        fields = '__all__'

# Custom validation to ensure:
#   - The student can book only 1 slot per day.
#   - Overlapping bookings are not allowed.
  
    
    def validate(self, data):
        student = self.context['request'].user
        booking_date = data.get('booking_date')
        infrastructure = data.get('infrastructure')

        # Check if the student has already booked a slot for the same day
        if Booking.objects.filter(student=student, booking_date=booking_date, status="Approved").exists():
            raise serializers.ValidationError("You can only book one slot per day.")

        # Check if the requested slot is available
        overlapping_booking = Booking.objects.filter(
            infrastructure=infrastructure,
            booking_date=booking_date,
            start_time__lt=data.get('end_time'),
            end_time__gt=data.get('start_time'),
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
    student = serializers.ReadOnlyField(source='student.username')
    infrastructure_name = serializers.ReadOnlyField(source='infrastructure.name')

    class Meta:
        model = Waitlist
        fields = '__all__'

"""
    Custom logic:
         -Add students to the waitlist in sequential order.
 """
def create(self, validated_data):
        infrastructure = validated_data['infrastructure']
        booking_date = validated_data['booking_date']
        start_time = validated_data['start_time']
        end_time = validated_data['end_time']

        # Determine the waitlist position
        position = Waitlist.objects.filter(
            infrastructure=infrastructure, booking_date=booking_date, start_time=start_time, end_time=end_time
        ).count() + 1

        validated_data['position'] = position
        return super().create(validated_data)


# defining a serilizer to convert Notification model instances into JSON format.
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'  

