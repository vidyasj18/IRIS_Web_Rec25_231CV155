from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from equipment.models import Equipment
from django.shortcuts import render, get_object_or_404, redirect
from infrastructure.models import Booking
from notifications.models import Notification
from django.http import JsonResponse

# Create your views here.
# Student Dashboard - Displays available equipment & facilities
@login_required
def student_dashboard(request):
    available_equipment = Equipment.objects.filter(availability='Available')
    available_facilities = Equipment.objects.filter(availability=True)
    notifications = Notification.objects.filter(user=request.user, is_read=False)

    return render(request, 'dashboard/student_dashboard.html', {
        'available_equipment': available_equipment,
        'available_facilities': available_facilities,
        'notifications':notifications
    })

# Equipment Booking View - allows students to book equipment.
@login_required
def book_equipment(request, equipment_id):
    equipment = get_object_or_404(Equipment, id=equipment_id)

    if request.method == "POST":
        quantity = int(request.POST['quantity'])
        if quantity > 1:
            return render(request, 'dashboard/book_equipment.html', {'equipment': equipment, 'error': 'One can not book more than one equipment.'})

        # Reduce equipment stock as one equipment is booked.
        equipment.quantity -= quantity
        equipment.save()

        # Send notification
        Notification.objects.create(user=request.user, message=f"You booked {quantity} {equipment.name}.")
        return JsonResponse({'success': True})

    return JsonResponse({'error': 'Invalid request'}, status=400)

# Facility Booking View - Lets students request to book a sports facility.
@login_required
def request_facility(request, facility_id):
    facility = get_object_or_404(Equipment, id=facility_id)

    if request.method == "POST":
        time_slot = request.POST['time_slot']
        booking = Booking.objects.create(user=request.user, facility=facility, time_slot=time_slot, status='Pending')
        
        # send notification
        Notification.objects.create(user=request.user, message=f"Your facility request for {facility.name} at {time_slot} is pending.")

        return JsonResponse({'success': True})

    return JsonResponse({'error': 'Invalid request'}, status=400)

# Cancel Booking Request - Enables students to cancel their facility booking.
@login_required
def cancel_request(request, request_id):
    booking = get_object_or_404(Booking, id=request_id, user=request.user)
    booking.delete()
    
    # Send notification
    Notification.objects.create(user=request.user, message="Your booking request has been cancelled.")

    return JsonResponse({'success': True})

# helps in fetching equipment list,bookings and notifications.
# this function helps in passing all the data to the front-end.
def dashboard_view(request):
    equipment = Equipment.objects.all()
    bookings = Booking.objects.all()
    notifications = Notification.objects.filter(user=request.user, is_read=False)

    return render(request, "student_dashboard.html", {
        "equipment": equipment,
        "bookings": bookings,
        "notifications": notifications
    })


# students can see the waitlist and position they are in the waitlist.
@login_required
def waitlist_booking(request, facility_id):
    facility = get_object_or_404(Equipment, id=facility_id)
    
    if request.method == "POST":
        approved_bookings = Booking.objects.filter(facility=facility, status='Approved').count()
        total_capacity = facility.capacity

        if approved_bookings >= total_capacity:
            # Get current waitlist position
            waitlist_count = Booking.objects.filter(facility=facility, status='Waitlisted').count()
            position = waitlist_count + 1

            # Add student to waitlist
            Booking.objects.create(user=request.user, facility=facility, status='Waitlisted')

            # Send notification
            Notification.objects.create(user=request.user, message=f"You are waitlisted for {facility.name}. Position: {position}")

            return JsonResponse({'success': True, 'waitlisted': True, 'position': position})

        return JsonResponse({'success': False, 'message': 'Slots are still available.'})

    return JsonResponse({'error': 'Invalid request'}, status=400)


# backend API for AJAX to fetch updates.
@login_required
def dashboard_updates(request):
    equipment = list(Equipment.objects.filter(availability='Available').values('id', 'name', 'quantity'))
    # facilities = list(Facility.objects.filter(is_available=True).values('id', 'name', 'location'))
    notifications = list(Notification.objects.filter(user=request.user, is_read=False).values('message'))

    return JsonResponse({
        "equipment": equipment,
        # "facilities": facilities,
        "notifications": notifications
    })
