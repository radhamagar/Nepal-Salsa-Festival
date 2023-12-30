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
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect("/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})




