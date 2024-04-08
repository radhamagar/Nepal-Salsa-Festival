from django import forms
from .models import *

class VolunteerForm(forms.ModelForm):
    class Meta():
        model = Volunteer



