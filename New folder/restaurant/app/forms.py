from django import forms
from .models import *

from django import forms
from datetime import datetime
from django.core.exceptions import ValidationError
from .models import Room, Person

class AvailabilityForm(forms.Form):
    check_in = forms.DateTimeField(
        required=True, input_formats=["%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M%Z"], widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    check_out = forms.DateTimeField(
        required=True, input_formats=["%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M%Z"], widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    # room_category = forms.ModelChoiceField(queryset=Room.objects.all())

    # def check_working_hours(self, start, end):
    #     check_in = self.cleaned_data.get('check_in')
    #     check_out = self.cleaned_data.get('check_out')
    #     if not(check_in < start and check_out < end):
    #         raise ValidationError(
    #             "Times beyond working hours, please enter value within working hours")
    #     else:
            # return self.cleaned_data

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'

# class BookingForm(forms.ModelForm):
#     class Meta:
#         model = Booking
#         fields = ['customer_name', 'customer_email', 'room',]
#         widgets = {
#             'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'customer_email': forms.EmailInput(attrs={'class': 'form-control'}),
#             'room': forms.Select(attrs={'class': 'form-control'}),
#         }

