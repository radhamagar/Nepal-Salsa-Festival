from django import forms
from authentication.models import SiteUser
from django.contrib.auth.forms import UserCreationForm
from django.forms import models

class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(models.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta():
        model = SiteUser

        fields = ("first_name", "last_name", "email", "ph_number", "password", "confirm_password")

        labels = {
                'first_name' :'First Name',
                'last_name' : 'Last Name',
                'email' : 'Email',
                'ph_number' : 'Phone Number',
                'password' : 'Password',
                'confirm_password' : 'Confirm Password'
        }
        widgets = {
            'password' : forms.PasswordInput,
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
