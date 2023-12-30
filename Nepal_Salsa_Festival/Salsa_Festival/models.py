from django import forms

class Register(forms.Form):
      first_name = forms.CharField(label="First Name", max_length=100)
      last_name = forms.CharField(label="Last Name", max_length=100)
      email = forms.CharField(label="Email")
        
