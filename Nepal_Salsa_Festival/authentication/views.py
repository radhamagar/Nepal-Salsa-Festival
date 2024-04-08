from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import LoginForm, RegisterForm
from .models import SiteUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages

# Create your views here.
def signin(request):
    form = LoginForm()

    if (request.method == "POST"):
        form = LoginForm(request.POST)
        if(form.is_valid()):
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)

            if (user is not None):
                if (user.is_superuser):
                    return redirect("admin/")
                if (user.is_staff):
                    return redirect(reverse("site_admin"))
                login(request, user)
                messages.success(request, "You're Sucessfully Logged In")
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
            print(form)

    context = {'form' : form}
    return render(request, 'authentication/signup.html', context)

def lost_password(request):
    if(request.method == "POST"):
        email = request.POST["email"]
        print(request.POST)
        try:
            user = SiteUser.objects.get(email=email)
            password = request.POST["password"]
            c_password = request.POST["c_password"]

            if (password == c_password and password != ""):
                user.password = make_password(password)
                user.save()
                return redirect(reverse("signin"))
        except:
            context = {
                "error" : "You Don't Have A User Registered With This Email, Check Again.."
            }
            return render(request, 'authentication/lost_password.html', context)
        context = {
            "user" : user
        }
        return render(request, 'authentication/lost_password.html', context)

    context = {
    }
    return render(request, 'authentication/lost_password.html', context)


def logout_view(request):
    logout(request)
    return redirect("home")
