from django import forms
from festivals.models import Festival, Schedule, DancePerformers, Musicians, Emcees, FoodVendors, Ticket, Order, FestivalImages
from Salsa_Festival.models import Sponsor, Volunteer, Feedback

class AdminFestivalForm(forms.ModelForm):
    class Meta:
        model = Festival
        fields = "__all__"

        widgets = {
            "date_time" : forms.widgets.DateInput(attrs={'type': 'date'})
        }

        labels = {
            "name" : "Festival Title",
            "feature_image" : "Feature Image"
        }
class AdminScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = "__all__"

        widgets = {
            "time" : forms.widgets.TimeInput(attrs={"type" : "time"})
        }

class AdminDancerForm(forms.ModelForm):
    class Meta:
        model = DancePerformers
        fields = "__all__"

class AdminMusicianForm(forms.ModelForm):
    class Meta:
        model = Musicians
        fields = "__all__"

class AdminEmceeForm(forms.ModelForm):
    class Meta:
        model = Emcees
        fields = "__all__"

class AdminFoodVendorForm(forms.ModelForm):
    class Meta:
        model = FoodVendors
        fields = "__all__"

class AdminTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = "__all__"

class AdminOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"

        widgets = {
            "order_date" : forms.widgets.DateInput(attrs={'type': 'date'}),
        }

        labels = {
            "order_name" : "Order Name (slug)"
        }

class AdminSponsorForm(forms.ModelForm):
    class Meta:
        model = Sponsor
        fields = "__all__"

class AdminVolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = "__all__"

class AdminFeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = "__all__"

class AdminFestivalImageForm(forms.ModelForm):
    class Meta:
        model = FestivalImages
        fields = "__all__"
