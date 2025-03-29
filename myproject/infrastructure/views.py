from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Booking, Notification
from .serializers import BookingSerializer, NotificationSerializer
from .models import Waitlist
from .serializers import WaitlistSerializer
from .models import Infrastructure, Booking
from .serializers import InfrastructureSerializer, BookingSerializer
from datetime import datetime, date
from django.http import JsonResponse
from notifications.utils import send_notification
from django.shortcuts import render
from .models import Infrastructure 


# Create your views here.

# This view allows users to view available sports facilities and lets admins add/update them.
class InfrastructureViewSet(viewsets.ModelViewSet):
    queryset = Infrastructure.objects.all()
    serializer_class = InfrastructureSerializer
    permission_classes = [IsAuthenticated]

    # Filtersavailable infrastructures
    def get_queryset(self):
        return Infrastructure.objects.filter(availability=True)

    # Allows admins to disable a facility temporarily.
    @action(detail=True, methods=['post'])
    def mark_under_maintenance(self, request, pk=None):
        infrastructure = self.get_object()
        infrastructure.availability = False
        infrastructure.save()
        return Response({'message': 'Infrastructure marked as under maintenance'}, status=status.HTTP_200_OK)


# This view allows students to book sports infrastructure and track their requests.
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    # Override create() to handle booking logic
    def create(self, request, *args, **kwargs):
        user = request.user
        infrastructure_id = request.data.get("infrastructure")
        start_time = request.data.get("start_time")

        # Check if user already booked today
        if Booking.objects.filter(user=user, start_time__date=timezone.now().date()).exists():
            return Response({'error': 'You can only book one slot per day'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if infrastructure is available
        infrastructure = get_object_or_404(Infrastructure, id=infrastructure_id)
        if not infrastructure.availability:
            return Response({'error': 'Infrastructure is not available'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the booking
        booking = Booking.objects.create(user=user, infrastructure=infrastructure, start_time=start_time)
        booking.save()

        # Send notification to user
        send_notification(user, "Your booking request has been submitted for approval.")

        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)


# This view allows users to view available sports facilities and lets admins add/update them.
class InfrastructureViewSet(viewsets.ModelViewSet):
    queryset = Infrastructure.objects.all()
    serializer_class = InfrastructureSerializer
    permission_classes = [IsAuthenticated]

    # Filter available infrastructures
    def get_queryset(self):
        return Infrastructure.objects.filter(availability=True)

    # Custom action to mark a facility as under maintenance (Admin only)
    @action(detail=True, methods=['post'])
    def mark_under_maintenance(self, request, pk=None):
        infrastructure = self.get_object()
        infrastructure.availability = False
        infrastructure.save()
        return Response({'message': 'Infrastructure marked as under maintenance'}, status=status.HTTP_200_OK)

# This view allows students to book sports infrastructure and track their requests.
# Checks if the student has already booked a slot for today.
# Ensures infrastructure is available before booking.
# Creates a booking and sends a notification.

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    # Override create() to handle booking logic
    def create(self, request, *args, **kwargs):
        user = request.user
        infrastructure_id = request.data.get("infrastructure")
        start_time = request.data.get("start_time")

        # Check if user already booked today
        if Booking.objects.filter(user=user, start_time__date=timezone.now().date()).exists():
            return Response({'error': 'You can only book one slot per day'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if infrastructure is available
        infrastructure = get_object_or_404(Infrastructure, id=infrastructure_id)
        if not infrastructure.availability:
            return Response({'error': 'Infrastructure is not available'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the booking
        booking = Booking.objects.create(user=user, infrastructure=infrastructure, start_time=start_time)
        booking.save()

        # Send notification to user
        send_notification(user, "Your booking request has been submitted for approval.")

        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)


# Admins can approve or reject bookings.
# Admin can approve or reject bookings.
# Sends a notification to the user after approval/rejection.

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def approve_booking(self, request, pk=None):
        booking = self.get_object()
        booking.status = 'approved'
        booking.save()

        send_notification(booking.user, "Your booking request has been approved.")
        return Response({'message': 'Booking approved'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def reject_booking(self, request, pk=None):
        booking = self.get_object()
        booking.status = 'rejected'
        booking.save()

        send_notification(booking.user, "Your booking request has been rejected.")
        return Response({'message': 'Booking rejected'}, status=status.HTTP_200_OK)


# If a student wants to cancel their booking, it must be approved by the admin.
# Students can request a cancellation.
# Admin must approve before cancellation is finalized.

    @action(detail=True, methods=['post'])
    def request_cancel(self, request, pk=None):
        booking = self.get_object()
        booking.status = 'cancel_pending'
        booking.save()

        send_notification(booking.infrastructure.manager, "A student has requested to cancel a booking.")
        return Response({'message': 'Cancellation request sent'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def confirm_cancel(self, request, pk=None):
        booking = self.get_object()

        if booking.status == 'cancel_pending':
            booking.delete()
            send_notification(booking.user, "Your booking has been canceled.")
            return Response({'message': 'Booking canceled successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'Booking cannot be canceled'}, status=status.HTTP_400_BAD_REQUEST)

# This view allows students to book sports infrastructure and track their waitlist.
# Students can join a waitlist if a slot is booked.
# They receive a notification when moved to an active booking.
class WaitlistViewSet(viewsets.ModelViewSet):
    queryset = Waitlist.objects.all()
    serializer_class = WaitlistSerializer

    @action(detail=True, methods=['post'])
    def join_waitlist(self, request, pk=None):
        infrastructure = self.get_object()
        user = request.user

        # Check if already on the waitlist
        if Booking.objects.filter(user=user, infrastructure=infrastructure, status='waitlisted').exists():
            return Response({'error': 'Already on the waitlist'}, status=status.HTTP_400_BAD_REQUEST)

        Booking.objects.create(user=user, infrastructure=infrastructure, status='waitlisted')
        send_notification(user, "You have been added to the waitlist.")
        return Response({'message': 'Added to waitlist'}, status=status.HTTP_201_CREATED)


# This sends notifications when a booking is approved or rejected.
# checks if the booking status has changed(approved/rejected).
# creates a notification for the user.

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def update(self, request, *args, **kwargs):
        """Custom update method to send notifications on approval/rejection."""
        instance = self.get_object()
        old_status = instance.status  # Get previous status

        response = super().update(request, *args, **kwargs)  # Perform update

        new_status = request.data.get('status')  # New status from request
        if old_status != new_status:  # If status changed
            message = f"Your booking for {instance.infrastructure.name} has been {new_status}."
            Notification.objects.create(user=instance.user, message=message)

        return response
    

def create_booking(request):
    if request.method == "POST":
        time_str = request.POST.get(default=timezone.now)  # Get "23:59:59" from request
        start_datetime = datetime.combine(date.today(), datetime.strptime(time_str, "%H:%M:%S").time())

        # Save to model
        booking = Booking.objects.create(start_time=start_datetime)
        return JsonResponse({"message": "Booking created successfully"})
    
def infrastructure_list(request):
    infrastructures = Infrastructure.objects.all()
    return render(request, "infrastructure/infrastructure_list.html", {"infrastructures": infrastructures})