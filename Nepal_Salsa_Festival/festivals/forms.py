from django import forms
from .models import Festival

class FestivalForm(forms.ModelForm):
    class Meta:
        model = Festival
        fields = (
                "name",
                "description",
                "past_description"
                )
        labels = {
                "name" : "Festival Name",
                "description" : "Festival Description",
                "past_description" : "Past Description"
            }
