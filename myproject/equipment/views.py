from django.shortcuts import render, redirect,get_object_or_404
from .models import Equipment, EquipmentRequest 
from .forms import EquipmentRequestForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from notifications.models import Notification

# This will display the list of equipments available. 
@login_required
def equipment_list(request):
    equipments = Equipment.objects.all()
    return render(request, 'equipment_list.html', {'equipments': equipments})

# admin can add or remove the equipments, courts or instruments based on their availability
# If the instrument is available then only they can add to this list. 
@login_required
def add_equipment(request):
    if request.method == 'POST':
        form = EquipmentRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipment added successfully!')
            return redirect('equipment_list')
    else:
        form = EquipmentRequestForm()
    return render(request, 'equipment/add_equipment.html', {'form': form})

# This will allow the user to request for the equipment.
# admin can see this request.
@login_required
def request_equipment(request):
    if request.method == 'POST':
        form = EquipmentRequestForm(request.POST)
        if form.is_valid():
            equipment_request = form.save(commit=False)
            equipment_request.user = request.user
            equipment_request.status = 'Pending'
            equipment_request.save()

            Notification.objects.create(
                user=request.user,
                message=f'New request for {equipment_request.equipment.name}.',
            )

            return redirect('equipment_list')
    else:
        form = EquipmentRequestForm()
    return render(request, 'equipment/request_equipment.html', {'form': form})

@login_required
def approve_request(request, request_id):
    """ Admin approves the equipment request and notifies the user """
    equipment_request = get_object_or_404(EquipmentRequest, id=request_id)
    equipment_request.status = 'Approved'
    equipment_request.save()

    # Create notification for the user
    Notification.objects.create(
        user=equipment_request.user,
        message=f'Your request for {equipment_request.equipment.name} has been approved.',
    )

    return redirect('view_requests')

@login_required
def reject_request(request, request_id):
    """ Admin rejects the equipment request and notifies the user """
    equipment_request = get_object_or_404(EquipmentRequest, id=request_id)
    equipment_request.status = 'Rejected'
    equipment_request.save()

    # Create notification for the user
    Notification.objects.create(
        user=equipment_request.user,
        message=f'Your request for {equipment_request.equipment.name} has been rejected.',
    )

    return redirect('view_requests')
