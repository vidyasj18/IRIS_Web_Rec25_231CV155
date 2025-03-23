# this file has the information about the form fields that are used in the equipment app

from django import forms
from .models import Equipment, EquipmentRequest

# This form is used to add or remove the equipment details.
# This form is used in the add_equipment view function.
class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'category', 'availability', 'quantity', 'condition']

# This form is used to request the equipment.
# This form is used in the request_equipment view function.
class EquipmentRequestForm(forms.ModelForm):
    class Meta:
        model = EquipmentRequest
        fields = ['quantity', 'duration']