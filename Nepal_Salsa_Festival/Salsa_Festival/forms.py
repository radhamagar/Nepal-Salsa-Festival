from django import forms
from .models import *

class VolunteerForm(forms.ModelForm):
    class Meta():
        model = Volunteer
        fields = "__all__"
        labels = {
            "festival" : "Select Festival",
            "email" : "Your Email",
            "ph_number" : "Your Phone Number"
        }



class SponsorForm(forms.ModelForm):
    class Meta():
        model =  Sponsor
        fields = "__all__"
        labels = {
            "festival" : "Select Festival",
            "email" : "Your Email",
            "ph_number" : "Your Phone Number"
        }

class FeedbackForm(forms.ModelForm):
    class Meta():
        model = Feedback
        fields = ('festival', 'message',)
        labels = {
            "festival" : "Feedback For Which Festival?",
            "first_name" : "Your First Name",
            "last_name" : "Your Last Name",
            "message" : "What Do You Have To Say About Nepal Salsa Festival?"
        }
