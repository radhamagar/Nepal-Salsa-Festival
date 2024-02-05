from django import forms
from authentication.models import User

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'password' : forms.PasswordInput,
            'email' : forms.EmailInput,
        }

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"
        widgets = {
            'password' : forms.PasswordInput,
            'c_password' : forms.PasswordInput,
            'email' : forms.EmailInput,
        }
        labels = {
                'first_name' :'First Name',
                'last_name' : 'Last Name',
                'email' : 'Email',
                'ph_number' : 'Phone Number',
                'password' : 'Password',
                'c_password' : 'Confirm Password'
        }
