from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, reverse
from festivals.models import Festival, Ticket, TicketAmount, Schedule, Order
from .forms import SponsorForm, VolunteerForm, FeedbackForm
from .models import Sponsor, Volunteer, Feedback
from django.utils.text import slugify
from authentication.models import SiteUser
import json
import requests
from django.forms.models import model_to_dict
from django.utils import timezone
from django.db.models import Max
from django.contrib import messages

# Create your views here.
def home(request):
    next_festival = Festival.objects.get(is_next=True)
    is_authenticated = False
    if(request.user.is_authenticated and not request.user.is_superuser and not request.user.is_staff):
        is_authenticated = request.user.is_authenticated

    feedbacks = Feedback.objects.all()
    sponsors = Sponsor.objects.filter(festival=next_festival)
    print(sponsors)

    context = {
        "next_festival" : next_festival,
        "is_authenticated" : is_authenticated,
        "feedbacks" : feedbacks,
        "sponsors" : sponsors,
    }

    return render(request, 'home.html', context)

def contact(request):
    is_authenticated = False
    if(request.user.is_authenticated and not request.user.is_superuser and not request.user.is_staff):
        is_authenticated = request.user.is_authenticated

    context = {
        "is_authenticated" : is_authenticated
    }
    return render(request, "contact.html", context)

def schedule(request):
    is_authenticated = False
    if(request.user.is_authenticated and not request.user.is_superuser and not request.user.is_staff):
        is_authenticated = request.user.is_authenticated

    next_festival = Festival.objects.get(is_next=True)
    schedule = Schedule.objects.filter(festival=next_festival)

    context = {
        "is_authenticated" : is_authenticated,
        "festival" : next_festival,
        "schedule" : schedule
    }
    return render(request, "schedule.html", context)

def participate(request):
    is_authenticated = False
    if(request.user.is_authenticated and not request.user.is_superuser and not request.user.is_staff):
        is_authenticated = request.user.is_authenticated

    next_festival = Festival.objects.get(is_next=True)
    sponsor_form = SponsorForm()
    volunteer_form = VolunteerForm()

    if (request.POST):
        request_dict = request.POST.dict()

        if (request_dict["which_form"] == "sponsor_form"):
            sponsor_form = SponsorForm(request.POST, request.FILES)

            if (sponsor_form.is_valid()):
                sponsor_form.save()
                messages.success(request, "Your Approach Has Sucessfully Been Registered..")
                return redirect(reverse("participate"))
            else:
                messages.error(request, "Invalid Data, Check Your Email")
                return redirect(reverse("participate"))
        else:
            volunteer_form = VolunteerForm(request.POST)

            if (volunteer_form.is_valid()):
                volunteer_form.save()
                messages.success(request, "Thank You For Showing Enthusiasm on Volunteering...")
                return redirect(reverse("participate"))
            else:
                messages.error(request, "Invalid Data, Check Your Email")
                return redirect(reverse("participate"))

    context = {
        "is_authenticated" : is_authenticated,
        "sponsor_form" : sponsor_form,
        "volunteer_form" : volunteer_form
    }

    return render(request, "participate.html", context)

def events(request):
    is_authenticated = False
    if(request.user.is_authenticated and not request.user.is_superuser and not request.user.is_staff):
        is_authenticated = request.user.is_authenticated

    now = timezone.now()
    upcoming_events = Festival.objects.filter(date_time__gt=now)
    context = {
        "upcoming_events" : upcoming_events,
        "is_authenticated" : is_authenticated
    }

    return render(request, "events.html", context)

def about(request):
    is_authenticated = False
    if(request.user.is_authenticated and not request.user.is_superuser and not request.user.is_staff):
        is_authenticated = request.user.is_authenticated

    context = {
        "is_authenticated" : is_authenticated
    }
    return render(request, "about.html", context)

def tickets(request, id):
    festival = Festival.objects.get(id=id)
    tickets = Ticket.objects.filter(festival__id=id)
    is_authenticated = False
    if(request.user.is_authenticated and not request.user.is_superuser and not request.user.is_staff):
        is_authenticated = request.user.is_authenticated

    context = {
        "tickets" : tickets,
        "festival" : festival,
        "is_authenticated" : is_authenticated
    }
    return render(request, "tickets.html", context)

def payment(request, id):
    is_authenticated = False
    if(request.user.is_authenticated and not request.user.is_superuser and not request.user.is_staff):
        is_authenticated = request.user.is_authenticated

    tickets = Ticket.objects.filter(festival__id=id)
    festival = Festival.objects.get(id=id)

    ticket_count = 0
    total_amount = 0

    tickets_dict = {}

    for ticket in tickets:
        if ticket.ticket_type == request.POST[slugify(ticket.ticket_type)]:
            ticket_amount = int(request.POST[f'{slugify(ticket.ticket_type)}-count'])
            ticket_total = ticket_amount * int(request.POST[f'{slugify(ticket.ticket_type)}-price'])
            ticket_count += ticket_amount
            total_amount += ticket_total
            tickets_dict[ticket.ticket_type] = {"amount" : ticket_amount, "price" : ticket.price}

    context = {
        "festival_id" : id,
        "ticket_count" : ticket_count,
        "total_amount" : total_amount,
        "tickets" : tickets_dict,
        "is_authenticated" : is_authenticated
    }

    request.session["tickets"] = tickets_dict

    return render(request, "payment.html", context)

def khalti_gateway(request, id):
    user = request.user;
    total = 0

    tickets_session = request.session.get("tickets")
    for key,value in tickets_session.items():
        total += value["amount"] * value["price"]

    orders= Order.objects.all()
    max_order = orders.aggregate(Max('id'))
    max_id = max_order["id__max"]

    try:
        if not user.is_superuser and not user.is_staff:
            full_name = f"{user.first_name} {user.last_name}"
            email = user.email
            phone = user.ph_number
            if(user.is_authenticated):
                url = "https://a.khalti.com/api/v2/epayment/initiate/"
                payload = json.dumps({
                    "return_url": f"http://localhost:8000/success?festival={id}&",
                    "website_url": "http://localhost:8000/",
                    #"amount": f"{total*100}",
                    "amount": f"{10*100}",

                    "purchase_order_id": f"{max_id}",
                    "purchase_order_name": f"{slugify(full_name)}-tickets-{max_id}",

                    "customer_info": {
                    "name": full_name,
                    "email": email,
                    "phone": phone,
                    }
                })

                headers = {
                    'Authorization': 'key 014f460ba3534c4aa4ed3102583413f4',
                    'Content-Type': 'application/json',
                }

                response = requests.request("POST", url, headers=headers, data=payload)
                payment_url = json.loads(response.text)["payment_url"];
                if(response.status_code == 200):
                    return redirect(payment_url);
                else:
                    return HttpResponse(response.text)
            else:
                return redirect("signin")
        else:
            return redirect("signin")

    except Exception as e:
        return redirect("signin");

def feedback(request):
    is_authenticated = False
    if(request.user.is_authenticated and not request.user.is_superuser and not request.user.is_staff):
        is_authenticated = request.user.is_authenticated
        
    form = FeedbackForm()

    if (is_authenticated):
        if (request.POST):
            user = SiteUser.objects.get(email=request.user.email)
            form = FeedbackForm(request.POST)
            if (form.is_valid()):
                instance = form.save(commit=False)
                instance.first_name = user.first_name
                instance.last_name = user.last_name
                instance.email = user.email
                instance.save()
                messages.success(request, "Thank You For Your Feedback!!")
                return redirect(reverse("feedback"))
    context = {
        "form" : form,
        "is_authenticated" : is_authenticated
    }

    return render(request, "feedback.html", context)
