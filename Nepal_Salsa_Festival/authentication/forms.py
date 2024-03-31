from django import forms
from authentication.models import SiteUser
from django.contrib.auth.forms import UserCreationForm
from django.forms import models
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        try:
            user = SiteUser.objects.get(email=self.cleaned_data["email"])
        except:
            raise ValidationError("User with this email doesn't exist. Try again or create new account")
        return self.cleaned_data["email"]


    def clean_password(self):
        try:
            user = SiteUser.objects.filter(email=self.cleaned_data["email"])
            if user.exists():
                if not (user[0].check_password(self.cleaned_data["password"])):
                    raise ValidationError("Your password is incorrect, please try again")
        except:
            raise ValidationError("Invalid Email or Password")
        return self.cleaned_data["password"]

class RegisterForm(models.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['ph_number'].required = True
        self.fields['password'].required = True
        self.fields['confirm_password'].required = True

    class Meta():
        model = SiteUser

        fields = ("first_name", "last_name", "email", "ph_number", "password", "confirm_password")

        labels = {
                'first_name' :'First Name',
                'last_name' : 'Last Name',
                'email' : 'Email',
                'ph_number' : 'Phone Number',
                'password' : 'Password',
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


    def clean_confirm_password(self):
        confirm_password  = self.cleaned_data["confirm_password"]
        password = self.cleaned_data["password"]

        if password != confirm_password:
            raise forms.ValidationError("Password and Confirm Password must be same")
        return confirm_password

