from django.shortcuts import render, redirect, reverse
from .forms import FestivalForm
from datetime import datetime, date
from .models import *
from django.forms import modelformset_factory
import json
import requests
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib import messages
import random
from django.template.loader import render_to_string
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Create your views here.


def festivals(request):
    is_authenticated = False
    if (request.user.is_authenticated and not request.user.is_superuser):
        is_authenticated = request.user.is_authenticated

    image_form_set = modelformset_factory(
        model=Festival, form=FestivalForm, extra=10)

    festival_images = {}

    festivals = Festival.objects.all()

    for festival in festivals:
        if (datetime.strptime(festival.date_time.strftime('%Y-%m-%d'), '%Y-%m-%d').date() < date.today()):
            image = festival.feature_image
            festival_images[festival.name] = {
                "image": image,
                "id": festival.id,
            }

    dance_performances = DancePerformers.objects.filter(
        festival__date_time__lt=datetime.now()).distinct()
    musicians = Musicians.objects.filter(
        festival__date_time__lt=datetime.now()).distinct()
    food_vendors = FoodVendors.objects.filter(
        festival__date_time__lt=datetime.now()).distinct()
    emcees = Emcees.objects.filter(
        festival__date_time__lt=datetime.now()).distinct()

    context = {
        "festival_images": festival_images,
        "dance_performances": dance_performances,
        "musicians": musicians,
        "food_vendors": food_vendors,
        "emcees": emcees,
        "is_authenticated": is_authenticated
    }

    return render(request, "festivals/festivals.html", context)


def festival_description(request, id):
    is_authenticated = False
    if (request.user.is_authenticated and not request.user.is_superuser):
        is_authenticated = request.user.is_authenticated

    festival = Festival.objects.get(id=id)
    images = FestivalImages.objects.filter(festival__id=id)

    context = {
        "festival": festival,
        "images": images,
        "is_authenticated": is_authenticated
    }
    return render(request, "festivals/festival_description.html", context)


def success(request):
    if (not request.user.is_anonymous):
        is_authenticated = False
        if (request.user.is_authenticated and not request.user.is_superuser):
            is_authenticated = request.user.is_authenticated
        tickets_session = request.session.get("tickets")
        ticket_keys = list(tickets_session.keys())

        order = Order()
        user = request.user
        orders = Order.objects.filter(user_id=user.id)
        festival_id = request.GET["festival"]
        order.user = SiteUser.objects.get(id=user.id)
        festival = Festival.objects.get(id=festival_id)
        order.festival = festival
        order.shipping_address = "Gaushala, Kathmandu"
        tickets = Ticket.objects.filter(festival_id=festival_id)
        live_stream = ""
        is_present = False
        order_name = request.GET["purchase_order_name"]
        order.order_name = order_name

        for ticket in tickets:
            if ticket.ticket_type in ticket_keys:
                if (ticket.ticket_type == "Live Streaming") and tickets_session[ticket.ticket_type]["amount"] != 0:
                    lobby_id = 0
                    for o in orders:
                        lobby_id = random.randint(1, 100)
                        if (o.lobby_id == lobby_id):
                            is_present = True
                            break
                    if not is_present:
                        order.lobby_id = lobby_id
                        live_stream = f"Your Unique Id to join the Live Stream is {order.lobby_id}"

                instance = TicketAmount()
                instance.ticket = ticket
                instance.count = tickets_session[ticket.ticket_type]["amount"]
                ticket.sold_tickets += instance.count
                ticket.save()
                instance.save()
                order.save()
                order.ticket_amounts.add(instance)

        context = {
            "order": order,
            "tickets": tickets_session,
            "is_authenticated": is_authenticated
        }

        if (order.lobby_id == 0):
            live_stream = ""

        subject = "Thank You For Purchasing Tickets"
        sender_email = 'radhabudhamagar8@gmail.com'
        live_link = f"http://localhost:8000/viewer/?room={order.lobby_id}"

        html_content = render_to_string("festivals/email.html", {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "order_name": order.order_name,
            "order_date": order.order_date,
            "live_stream": live_stream,
            "live_link": live_link
        })

        send_list = [user.email,]

        send_mail(subject, '', sender_email, [
                  "radhabudhamagar8@gmail.com",], html_message=html_content)

        if "tickets" in request.session:
            del request.session["tickets"]

        messages.success(request, f"Thank You For Purchasing The Tickets!!!!!")
        return render(request, "success.html", context)
    else:
        return redirect(reverse("error", kwargs={'code': 401}))
