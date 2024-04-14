from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import LoginForm, RegisterForm
from .models import SiteUser
from festivals.models import Order
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
                messages.success(request, f"Hello {user.first_name} {user.last_name}, You're Sucessfully Logged In")
                return redirect(reverse('home'))

    context = {'form' : form}
    return render(request, 'authentication/signin.html', context)

def signup(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            messages.success(request, f"Hello {form.cleaned_data['first_name']} {form.cleaned_data['last_name']}, Registratered Sucessfully, Please Log In")
            form.save()
            return redirect(reverse('signin'))
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
                messages.success(request,"Your password has been sucessfully changed. Login With New Password")
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
    messages.success(request, "You're logged out sucessfully");
    return redirect("home")

def profile(request):
    is_authenticated = False
    if(request.user.is_authenticated and not request.user.is_superuser):
        is_authenticated = request.user.is_authenticated
    user = SiteUser.objects.get(email=request.user.email)
    orders = Order.objects.filter(user_id=user.id)

    print(orders)
    context = {
        "user" : user,
        "is_authenticated" : is_authenticated,
        "orders": orders
    }

    if (request.method == "POST"):
        new_first_name = request.POST["first_name"]
        new_last_name = request.POST["last_name"]
        new_ph_number = request.POST["ph_number"]
        new_email = request.POST["email"]

        user.first_name = new_first_name
        user.last_name = new_last_name
        user.ph_number = new_ph_number
        user.email = new_email

        user.save()
        messages.success(request, f"Profile Updated Sucessfully")

    return render(request, "authentication/profile.html", context)
