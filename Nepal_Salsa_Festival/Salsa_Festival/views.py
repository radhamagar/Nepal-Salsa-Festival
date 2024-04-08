from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from festivals.models import Festival, Ticket, TicketAmount, Schedule
from django.utils.text import slugify
from authentication.models import SiteUser
import json
import requests
from django.forms.models import model_to_dict
from django.utils import timezone

# Create your views here.
def home(request):
    next_festival = Festival.objects.get(is_next=True)
    is_authenticated = False
    if(request.user.is_authenticated and not request.user.is_superuser):
        is_authenticated = request.user.is_authenticated

    context = {
        "next_festival" : next_festival,
        "is_authenticated" : is_authenticated,
    }

    return render(request, 'home.html', context)

def contact(request):
    is_authenticated = False
    if(request.user.is_authenticated and not request.user.is_superuser):
        is_authenticated = request.user.is_authenticated

    context = {
        "is_authenticated" : is_authenticated
    }
    return render(request, "contact.html", context)

def schedule(request):
    is_authenticated = False
    if(request.user.is_authenticated and not request.user.is_superuser):
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
    if(request.user.is_authenticated and not request.user.is_superuser):
        is_authenticated = request.user.is_authenticated

    context = {
        "is_authenticated" : is_authenticated
    }

    if (request.POST):
        print(request.POST)
    return render(request, "participate.html", context)

def events(request):
    is_authenticated = False
    if(request.user.is_authenticated and not request.user.is_superuser):
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
    if(request.user.is_authenticated and not request.user.is_superuser):
        is_authenticated = request.user.is_authenticated

    context = {
        "is_authenticated" : is_authenticated
    }
    return render(request, "about.html", context)

def tickets(request, id):
    festival = Festival.objects.get(id=id)
    tickets = Ticket.objects.filter(festival__id=id)
    is_authenticated = False
    if(request.user.is_authenticated and not request.user.is_superuser):
        is_authenticated = request.user.is_authenticated

    context = {
        "tickets" : tickets,
        "festival" : festival,
        "is_authenticated" : is_authenticated
    }
    return render(request, "tickets.html", context)

def payment(request, id):
    is_authenticated = False
    if(request.user.is_authenticated and not request.user.is_superuser):
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
    user = request.user
    try:
        if not user.is_superuser:
            full_name = f"{user.first_name} {user.last_name}"
            email = user.email
            phone = user.ph_number
            if(user.is_authenticated):
                url = "https://a.khalti.com/api/v2/epayment/initiate/"
                payload = json.dumps({
                    "return_url": f"http://localhost:8000/success?festival={id}&",
                    "website_url": "http://localhost:8000/",
                    "amount": f"{1000*100}",

                    "purchase_order_id": "Order01",
                    "purchase_order_name": "test",

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
                payment_url = json.loads(response.text)["payment_url"]

                if(response.status_code == 200):
                    return redirect(payment_url)
                else:
                    return HttpResponse(response.text)
            else:
                return redirect("signin")
        else:
            return redirect("signin")

    except:
        return redirect("signin");

