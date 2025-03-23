from django.shortcuts import render, redirect
from .models import Equipment, EquipmentRequest
from .forms import EquipmentForm, EquipmentRequestForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# This will display the list of equipments available. 
@login_required
def equipment_list(request):
    equipments = Equipment.objects.all()
    return render(request, 'equipment/equipment_list.html', {'equipments': equipments})

# admin can add or remove the equipments, courts or instruments based on their availability
# If the instrument is available then only they can add to this list. 
@login_required
def add_equipment(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipment added successfully!')
            return redirect('equipment_list')
    else:
        form = EquipmentForm()
    return render(request, 'equipment/add_equipment.html', {'form': form})

# This will allow the user to request for the equipment.
# admin can see this request.
@login_required
def request_equipment(request, equipment_id):
    equipment = Equipment.objects.get(id=equipment_id)
    if request.method == 'POST':
        form = EquipmentRequestForm(request.POST)
        if form.is_valid():
            equipment_request = form.save(commit=False)
            equipment_request.user = request.user
            equipment_request.equipment = equipment
            equipment_request.save()
            messages.success(request, 'Equipment request submitted successfully!')
            return redirect('equipment_list')
    else:
        form = EquipmentRequestForm()
    return render(request, 'equipment/request_equipment.html', {'form': form, 'equipment': equipment})