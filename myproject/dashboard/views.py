from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from equipment.models import Equipment
from django.shortcuts import render, get_object_or_404, redirect
from infrastructure.models import Booking, WaitlistBooking
from notifications.models import Notification
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from infrastructure.models import Infrastructure
from infrastructure.models import FacilityRequest
import json
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync




# Create your views here.
# Student Dashboard - Displays available equipment & facilities
@login_required
def student_dashboard(request):
    user = request.user
    available_equipment = Equipment.objects.filter(availability=True)
    available_facilities = Infrastructure.objects.filter(availability=True)
    waitlist = WaitlistBooking.objects.filter(user=user)
    notifications = Notification.objects.filter(user=user, is_read=False)
    requests = Booking.objects.filter(user=user)  # Fetch user's bookings

    return render(request, 'student_dashboard.html', {
        'available_equipment': available_equipment,
        'available_facilities': available_facilities,
        'waitlist': waitlist,
        'notifications':notifications,
        'requests': requests,
    })

# Equipment Booking View - allows students to book equipment.
@login_required
def book_equipment(request, equipment_id):
    if request.method == "POST":
    #     equipment = get_object_or_404(Equipment, id=equipment_id)

    #     # Ensure user can only book 1 at a time
    #     if Booking.objects.filter(user=request.user, equipment=equipment, status='pending').exists():
    #         return JsonResponse({'error': 'You already have a pending booking for this equipment'}, status=400)

    #     # Reduce equipment stock as one equipment is booked.
    #     if equipment.quantity > 0:
    #         equipment.quantity -= 1
    #         equipment.save()

    #         Booking.objects.create(user=request.user, equipment=equipment, status='pending')

    #         # Send notification
    #         Notification.objects.create(user=request.user, message=f"You booked {equipment.name}.")
    #         return JsonResponse({'success': True})
        
    #     return JsonResponse({'error': 'Equipment is out of stock'}, status=400)

    # return JsonResponse({'error': 'Invalid request'}, status=400)
        try:
            data = json.loads(request.body)
            requested_slot = data.get("requested_slot")

            if not requested_slot:
                return JsonResponse({"success": False, "error": "Requested slot is required"}, status=400)

            # Convert requested_slot to a Python datetime object
            requested_slot = parse_datetime(requested_slot)
            if requested_slot is None:
                return JsonResponse({"success": False, "error": "Invalid date format"}, status=400)

            # Create the booking
            booking = Booking.objects.create(
                user=request.user,
                equipment_id=equipment_id,
                requested_slot=requested_slot,
                status="Pending"
            )
            return JsonResponse({"success": True})
        
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

# Facility Booking View - Lets students request to book a sports facility.
@login_required
def request_facility(request, facility_id):
    facility = get_object_or_404(Infrastructure, id=facility_id)

    if request.method == "POST":
        time_slot = request.POST['time_slot']
        # create facility request
        Booking.objects.create(user=request.user, facility=facility, time_slot=time_slot, status='pending')

        # send notification
        Notification.objects.create(user=request.user, message=f"Your facility request for {facility.name} at {time_slot} is pending.")

        return JsonResponse({'success': True})

    return JsonResponse({'error': 'Invalid request'}, status=400)

# Cancel Booking Request - Enables students to cancel their facility booking.
@login_required
def cancel_request(request, request_id):
    booking = get_object_or_404(Booking, id=request_id, user=request.user)

    if booking.status == 'pending':  # Allow cancellation only if still pending
        booking.delete()
        Notification.objects.create(user=request.user, message="Your booking request has been cancelled.")
        return JsonResponse({'success': True})

    return JsonResponse({'error': 'Request cannot be canceled'}, status=400)

    

# students can see the waitlist and position they are in the waitlist.
@login_required
def waitlistBooking(request, facility_id):
    equipment = get_object_or_404(Equipment, id=facility_id)
    
    if request.method == "POST":
        approved_bookings = Booking.objects.filter(equipment=equipment, status='Approved').count()
        total_capacity = equipment.capacity

        if approved_bookings >= total_capacity:
            # Get current waitlist position
            waitlist_count = WaitlistBooking.objects.filter(equipment=equipment, status='Waitlisted').count()
            position = waitlist_count + 1

            # Add student to waitlist
            WaitlistBooking.objects.create(user=request.user, equipment=equipment, status='Waitlisted')

            # Send notification
            Notification.objects.create(user=request.user, message=f"You are waitlisted for {equipment.name}. Position: {position}")

            return JsonResponse({'success': True, 'waitlisted': True, 'position': position})

        return JsonResponse({'success': False, 'message': 'Slots are still available.'})

    return JsonResponse({'error': 'Invalid request'}, status=400)



# helps in fetching equipment list,bookings and notifications.
# this function helps in passing all the data to the front-end.
def dashboard_view(request):
    equipment_list = Equipment.objects.all()  # Fetch all equipment
    # Fetch user requests
    requests = Booking.objects.filter(user=request.user) 
    
    waitlist = WaitlistBooking.objects.filter(user=request.user) 
    notifications = Notification.objects.filter(user=request.user)  # Fetch user notifications
    
    return render(request, 'dashboard.html', {
        'equipment_list': equipment_list,
        'requests': requests,
        'waitlist': waitlist,
        'notifications': notifications
    })
   


# backend API for AJAX to fetch updates.
@login_required
def dashboard_updates(request):
    equipment = list(Equipment.objects.filter(availability=True).values('id', 'name', 'quantity','availability'))
    facilities = list(Infrastructure.objects.filter(availability=True).values('id', 'name'))
    notifications = list(Notification.objects.filter(user=request.user, is_read=False).values('message'))

    return JsonResponse({
        "equipment": equipment,
        "facilities": facilities,
        "notifications": notifications
    })

@login_required
def user_bookings(request):
    bookings = Booking.objects.filter(user=request.user).values(
        "id", "equipment__name", "status", "requested_slot"
    )
    return JsonResponse(list(bookings), safe=False)


# Check if user is admin 
def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def custom_admin_dashboard(request):
    # Fetch pending equipment bookings
    bookings = Booking.objects.filter(status="Pending")  # Ensure status is 'Pending'
    
    # Fetch waitlist data
    waitlist = WaitlistBooking.objects.all()  # Modify as per your requirement

    # Fetch notifications
    notifications = Notification.objects.all()

    return render(request, "admin_dashboard.html", {
        "bookings": bookings,
        "waitlist": waitlist,
        "notifications": notifications
    })

@csrf_exempt
def update_booking_status(request, booking_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            action = data.get("status")  # "Approved" or "Rejected"

            # Ensure booking exists
            booking = Booking.objects.get(id=booking_id)
            booking.status = action
            booking.save()

            return JsonResponse({"success": True})

        except Booking.DoesNotExist:
            return JsonResponse({"success": False, "error": "Booking not found"}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON format"}, status=400)

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)