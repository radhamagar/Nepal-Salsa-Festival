from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import LoginForm, RegisterForm
from .models import SiteUser
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def signin(request):
    form = LoginForm()

    if (request.method == "POST"):
        form = LoginForm(request.POST)

        if(form.is_valid()):
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            print(authenticate(request, email=email, password=password))

            if (user is not None):
                login(request, user)
                return redirect(reverse('home'))

    context = {'form' : form}
    return render(request, 'authentication/signin.html', context)

def signup(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(reverse('home'))
        else:
            print("Invalid")

    context = {'form' : form}
    return render(request, 'authentication/signup.html', context)

def logout_view(request):
    logout(request)
    return redirect("home")
