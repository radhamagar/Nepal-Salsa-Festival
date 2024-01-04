from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from .forms import RegisterForm


# Create your views here.
def home(request):
    return render(request, template_name='home.html')

def register(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        first_name=request.POST.get(first_name=first_name)
        last_name=request.POST.get(last_name=last_name)
        email=request.POST.get(email=email)
        password=request.POST.get(password=password)
        confirm_password=request.POST.get(confirm_password=confirm_password)
        ph_no=request.POST.get(ph_no=ph_no)
        # check whether it's valid:
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})




