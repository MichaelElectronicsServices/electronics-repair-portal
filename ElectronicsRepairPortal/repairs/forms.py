from django import forms
from .models import RepairTicket, Part, Customer, Estimate,Item_description, Schedule, TicketUpdate

class RepairTicketForm(forms.ModelForm):
    class Meta:
        model = RepairTicket
        fields = ['status','warranty']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name',
		'last_name',
     	    'email',
            'phone',
            'address',
            'city',
            'zip_code',
        ]

class ItemDescriptionForm(forms.ModelForm):
    class Meta:
        model = Item_description
        fields = [
            'brand',
            'serial_number',
            'model_number',
            'issue_description',
        ]
class PartOrderForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = ['part_number','part_description', 'cost', 'ordered']

class EstimateForm(forms.ModelForm):
    class Meta:
        model = Estimate
        fields = ['parts_cost', 'labor_total', 'approved']



class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['scheduled_for', 'confirmed']


class TicketUpdateForm(forms.ModelForm):
    class Meta:
        model = TicketUpdate
        fields = ['message', 'internal_only']
