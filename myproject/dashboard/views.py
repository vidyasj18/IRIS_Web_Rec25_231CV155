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


# Create your views here.
# Student Dashboard - Displays available equipment & facilities
@login_required
def student_dashboard(request):
    user = request.user
    available_equipment = Equipment.objects.filter(availability=True)
    available_facilities = Infrastructure.objects.filter(availability=True)
    waitlist = WaitlistBooking.objects.filter(user=user)
    notifications = Notification.objects.filter(user=user, is_read=False)

    return render(request, 'student_dashboard.html', {
        'available_equipment': available_equipment,
        'available_facilities': available_facilities,
        'waitlist': waitlist,
        'notifications':notifications,
    })

# Equipment Booking View - allows students to book equipment.
@login_required
def book_equipment(request, equipment_id):
    if request.method == "POST":
        equipment = get_object_or_404(Equipment, id=equipment_id)

        # Ensure user can only book 1 at a time
        if Booking.objects.filter(user=request.user, equipment=equipment, status='pending').exists():
            return JsonResponse({'error': 'You already have a pending booking for this equipment'}, status=400)

        # Reduce equipment stock as one equipment is booked.
        if equipment.quantity > 0:
            equipment.quantity -= 1
            equipment.save()

            Booking.objects.create(user=request.user, equipment=equipment, status='pending')

            # Send notification
            Notification.objects.create(user=request.user, message=f"You booked {equipment.name}.")
            return JsonResponse({'success': True})
        
        return JsonResponse({'error': 'Equipment is out of stock'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)

# Facility Booking View - Lets students request to book a sports facility.
@login_required
def request_facility(request, facility_id):
    facility = get_object_or_404(FacilityRequest, id=facility_id)

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
    equipment = get_object_or_404(equipment, id=facility_id)
    
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
    requests = Booking.objects.filter(user=request.user) if hasattr(Booking, 'user') else Booking.objects.all()
    
    waitlist = WaitlistBooking.objects.filter(user=request.user) if hasattr(waitlist, 'user') else waitlist.objects.all() # Fetch user waitlist
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
    facilities = list(Equipment.objects.filter(is_available=True).values('id', 'name'))
    notifications = list(Notification.objects.filter(user=request.user, is_read=False).values('message'))

    return JsonResponse({
        "equipment": equipment,
        "facilities": facilities,
        "notifications": notifications
    })
