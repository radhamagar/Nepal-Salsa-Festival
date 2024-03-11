from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from festivals.models import Festival, Ticket, Bill
from django.utils.text import slugify
from authentication.models import SiteUser
import json
import requests
from django.forms.models import model_to_dict

# Create your views here.
def home(request):
    next_festival = Festival.objects.get(is_next=True)
    is_authenticated = False
    if(request.user.is_authenticated):
        is_authenticated = request.user.is_authenticated

    context = {
        "next_festival" : next_festival,
        "is_authenticated" : is_authenticated,
    }
    return render(request, 'home.html', context)

def contact(request):
    context = {}
    return render(request, "contact.html", context)

def schedule(request):
    context = {}
    return render(request, "schedule.html", context)

def about(request):
    context = {}
    return render(request, "about.html", context)

def tickets(request, id):
    festival = Festival.objects.get(id=id)
    tickets = Ticket.objects.filter(festival__id=id)
    context = {
        "tickets" : tickets,
        "festival" : festival,
    }
    return render(request, "tickets.html", context)

def payment(request, id):
    tickets = Ticket.objects.filter(festival__id=id)
    festival = Festival.objects.get(id=id)
    ticket_count = 0
    total_amount = 0

    for ticket in tickets:
        if ticket.ticket_type == request.POST[slugify(ticket.ticket_type)]:
            ticket_amount = int(request.POST[f'{slugify(ticket.ticket_type)}-count'])
            ticket_total = ticket_amount * int(request.POST[f'{slugify(ticket.ticket_type)}-price'])
            ticket_count += ticket_amount
            total_amount += ticket_total


    context = {
        "ticket_count" : ticket_count,
        "total_amount" : total_amount
    }

    return render(request, "payment.html", context)

def khalti_gateway(request):


    if(request.user.is_authenticated):
        user = request.user
        full_name = f"{user.first_name if user.first_name else ''} {user.last_name if user.last_name else ''}"
        email = user.email
        phone = user.ph_number

        url = "https://a.khalti.com/api/v2/epayment/initiate/"
        payload = json.dumps({
            "return_url": "http://localhost:8000/success",
            "website_url": "http://localhost:8000/",
            "amount": f"{10*100}",

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
        payment_url = json.loads(response.text)

        if(response.status_code == 200):
            return redirect(payment_url["payment_url"]);
        else:
            return HttpResponse(response.text)
    else:
        return redirect("signin")
