from django.shortcuts import render, redirect
from .forms import FestivalForm
from datetime import datetime, date
from .models import *
from django.forms import modelformset_factory
import json
import requests
from django.http import HttpResponse
from django.core.mail import send_mail

# Create your views here.
def festivals(request):
    is_authenticated = False
    if(request.user.is_authenticated and not request.user.is_superuser):
        is_authenticated = request.user.is_authenticated

    image_form_set = modelformset_factory(model=Festival, form=FestivalForm, extra=10)

    festival_images = {}

    festivals = Festival.objects.all()

    for festival in festivals:
        if(datetime.strptime(festival.date_time.strftime('%Y-%m-%d'), '%Y-%m-%d').date() < date.today()):
            image = festival.feature_image
            festival_images[festival.name] = {
                    "image" : image,
                    "id" : festival.id,
            }

    dance_performances = DancePerformers.objects.filter(festival__date_time__lt=datetime.now()).distinct()
    musicians = Musicians.objects.filter(festival__date_time__lt=datetime.now()).distinct()
    food_vendors = FoodVendors.objects.filter(festival__date_time__lt=datetime.now()).distinct()
    emcees = Emcees.objects.filter(festival__date_time__lt=datetime.now()).distinct()

    context = {
        "festival_images" : festival_images,
        "dance_performances" : dance_performances,
        "musicians" : musicians,
        "food_vendors" : food_vendors,
        "emcees" : emcees,
        "is_authenticated" : is_authenticated
    }

    return render(request, "festivals/festivals.html",context)

def festival_description(request, id):
    is_authenticated = False
    if(request.user.is_authenticated and not request.user.is_superuser):
        is_authenticated = request.user.is_authenticated

    festival = Festival.objects.get(id=id)
    images = FestivalImages.objects.filter(festival__id=id)

    context = {
        "festival" : festival,
        "images" : images,
        "is_authenticated" : is_authenticated
    }
    return render(request, "festivals/festival_description.html", context)

def success(request):
    if (not request.user.is_anonymous):
        is_authenticated = False
        if(request.user.is_authenticated and not request.user.is_superuser):
            is_authenticated = request.user.is_authenticated
        tickets_session = request.session.get("tickets")
        ticket_keys = list(tickets_session.keys())
        order = Order()
        user = request.user
        festival_id = request.GET["festival"]
        order.user = SiteUser.objects.get(id=user.id)
        festival = Festival.objects.get(id=festival_id)
        order.festival = festival
        order.shipping_address = "Gaushala, Kathmandu"
        tickets = Ticket.objects.filter(festival_id=festival_id)

        for ticket in tickets:
            if ticket.ticket_type in ticket_keys:
                instance = TicketAmount()
                instance.ticket = ticket
                instance.count = tickets_session[ticket.ticket_type]["amount"]
                ticket.sold_tickets += instance.count
                ticket.save()
                instance.save()
                order.save()
                order.ticket_amounts.add(instance)

        context = {
            "order" : order,
            "tickets" : tickets_session,
            "is_authenticated" : is_authenticated
        }

        subject = 'Thank You For Purchasing The Tickets'
        message = f'''
            We will be happy to meet you at the venue!
        '''
        sender_email = 'radhabudhamagar8@gmail.com'
        print(user.email)

        send_mail(subject, message, sender_email, ["radhabudhamagar8@gmail.com",])

        if "tickets" in request.session:
            del request.session["tickets"]

        return render(request, "success.html", context)
    else:
        return  HttpResponse("You are not authenticated.")

