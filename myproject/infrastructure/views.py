from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from datetime import datetime, date
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view

from .models import Infrastructure, Booking, WaitlistBooking, Notification
from .serializers import InfrastructureSerializer, BookingSerializer, WaitlistSerializer
from notifications.utils import send_notification



# Create your views here.

# This view allows users to view available sports facilities and lets admins add/update them.
class InfrastructureViewSet(viewsets.ModelViewSet):
    queryset = Infrastructure.objects.all()
    serializer_class = InfrastructureSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Infrastructure.objects.filter(availability=True)

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
        infrastructure = request.data.get("infrastructure")
        start_time = request.data.get("start_time")

        # Check if user already booked today
        if Booking.objects.filter(user=user, start_time__date=timezone.now().date()).exists():
            return Response({'error': 'You can only book one slot per day'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if infrastructure is available
        infrastructure = get_object_or_404(Infrastructure, id= "infrastructure_id")
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
    
    @action(detail=True, methods=['post'])
    def reject_booking(self, request, pk=None):
        booking = self.get_object()
        booking.status = 'rejected'
        booking.save()
        send_notification(booking.user, "Your booking request has been rejected.")
        return Response({'message': 'Booking rejected'}, status=status.HTTP_200_OK)

# This view allows students to book sports infrastructure and track their waitlist.
# Students can join a waitlist if a slot is booked.
# They receive a notification when moved to an active booking.
class waitlistViewSet(viewsets.ModelViewSet):
    queryset = WaitlistBooking.objects.all()
    serializer_class = WaitlistSerializer

    @action(detail=True, methods=['post'])
    def join_waitlist(self, request, pk=None):
        infrastructure = self.get_object()
        user = request.user

        # Check if already on the waitlist
        if WaitlistBooking.objects.filter(user=user, infrastructure=infrastructure).exists():
            return Response({'error': 'Already on the waitlist'}, status=status.HTTP_400_BAD_REQUEST)

        waitlist_entry = WaitlistBooking.objects.create(user=user, infrastructure=infrastructure)
        send_notification(user, "You have been added to the waitlist.")
        return Response({'message': 'Added to waitlist'}, status=status.HTTP_201_CREATED)
    


@login_required
def add_to_waitlist(request, facility_id):
    """Adds the user to the waitlist if the facility is full."""
    user = request.user
    facility = get_object_or_404(Infrastructure, id=facility_id)

    # Count approved bookings
    approved_bookings = facility.booking_set.filter(status='Approved').count()

    # If facility is full, add to waitlist
    if approved_bookings >= facility.capacity:
        position = WaitlistBooking.objects.filter(equipment=facility).count() + 1
        WaitlistBooking.objects.create(user=user, infrastructure=facility, position=position)
        Notification.objects.create(user=user, message=f"You are waitlisted for {facility.name}. Position: {position}")


        return JsonResponse({'success': True, 'waitlisted': True, 'position': position})

    return JsonResponse({'success': False, 'message': 'Slots are still available.'})


# shows the infrastructure list.
def infrastructure_list(request):
    infrastructures = Infrastructure.objects.all()
    return render(request, "index.html", {"infrastructures": infrastructures})

@api_view(['GET'])
def user_bookings(request):
    user = request.user
    bookings = Booking.objects.filter(user=user).order_by('-requested_slot')
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)