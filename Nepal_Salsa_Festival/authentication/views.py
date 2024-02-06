from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import LoginForm, RegisterForm
from .models import User

# Create your views here.
def signin(request):
    form = LoginForm()

    if (request.POST):
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.get(email=email)

        if (user):
            if (password == user.password):
                print('Logged In Sucessfully')
                return redirect(reverse('home'))

    context = {'form' : form}
    return render(request, 'authentication/signin.html', context)

def signup(request):
    form = RegisterForm()

    if (request.POST):
        form = RegisterForm(request.POST)
        form.save()
        return redirect(reverse('home'))

    context = {'form' : form}
    return render(request, 'authentication/signup.html', context)
