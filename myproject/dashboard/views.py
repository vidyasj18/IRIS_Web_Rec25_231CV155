from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from equipment.models import Equipment
from django.shortcuts import render, get_object_or_404, redirect
from infrastructure.models import Booking

# Create your views here.
# Student Dashboard - Displays available equipment & facilities
@login_required
def student_dashboard(request):
    available_equipment = Equipment.objects.filter(availability='Available')
    available_facilities = Equipment.objects.filter(availability=True)

    return render(request, 'dashboard/student_dashboard.html', {
        'available_equipment': available_equipment,
        'available_facilities': available_facilities
    })

# Equipment Booking View - allows students to book equipment.
@login_required
def book_equipment(request, equipment_id):
    equipment = get_object_or_404(Equipment, id=equipment_id)

    if request.method == "POST":
        quantity = int(request.POST['quantity'])
        if quantity > equipment.quantity:
            return render(request, 'dashboard/book_equipment.html', {'equipment': equipment, 'error': 'Not enough quantity available.'})

        # Reduce equipment stock
        equipment.quantity -= quantity
        equipment.save()
        return redirect('student_dashboard')

    return render(request, 'dashboard/book_equipment.html', {'equipment': equipment})

# Facility Booking View - Lets students request to book a sports facility.
@login_required
def request_facility(request, facility_id):
    facility = get_object_or_404(Equipment, id=facility_id)

    if request.method == "POST":
        time_slot = request.POST['time_slot']
        Booking.objects.create(user=request.user, facility=facility, time_slot=time_slot, status='Pending')
        return redirect('student_dashboard')

    return render(request, 'dashboard/request_facility.html', {'facility': facility})

# Cancel Booking Request - Enables students to cancel their facility booking.
@login_required
def cancel_request(request, request_id):
    booking = get_object_or_404(Booking, id=request_id, user=request.user)
    booking.delete()
    return redirect('student_dashboard')
