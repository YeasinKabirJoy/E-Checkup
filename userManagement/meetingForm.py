from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from .models import Meeting
from django import forms


class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['s_time',]
        widgets = {
            's_time':TimePickerInput(format='%I:%M %p'),
        }