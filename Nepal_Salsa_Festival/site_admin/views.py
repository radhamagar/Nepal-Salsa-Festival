from django.shortcuts import render, redirect
from django.urls import reverse
from festivals.models import Festival, Schedule, DancePerformers, Musicians, Emcees, FoodVendors, Ticket, Order, FestivalImages
from Salsa_Festival.models import Sponsor, Volunteer, Feedback
from .forms import AdminFestivalForm, AdminScheduleForm, AdminDancerForm, AdminMusicianForm, AdminEmceeForm, AdminFoodVendorForm, AdminTicketForm, AdminOrderForm, AdminSponsorForm, AdminVolunteerForm, AdminFeedbackForm, AdminFestivalImageForm
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from collections import defaultdict
from authentication.models import SiteUser
from datetime import datetime


# Create your views here.
def site_admin(request):
    return redirect(reverse("signin"))


def is_future(user_date):
    current_date = datetime.now()
    return current_date > user_date


def dashboard(request):
    is_authenticated = False
    current_date = datetime.now()
    if (request.user.is_authenticated and not request.user.is_superuser and request.user.is_staff):
        is_authenticated = request.user.is_authenticated

    if (is_authenticated):
        user = SiteUser.objects.get(email=request.user.email)
        festivals = Festival.objects.all()
        context = {
            "festivals": festivals,
            "is_authenticated": is_authenticated,
            "user": user,
            "current_date": current_date
        }
        return render(request, 'site_admin/dashboard.html', context)
    else:
        messages.error(
            request, "You are not authenticated, sign in as a staff")
        return redirect(reverse("signin"))


def site_admin_festivals(request):
    is_authenticated = False
    if (request.user.is_authenticated and not request.user.is_superuser and request.user.is_staff):
        is_authenticated = request.user.is_authenticated

    festivals = Festival.objects.all()
    festival_form = AdminFestivalForm()

    context = {
        "festivals": festivals,
        "form": festival_form,
        "is_authenticated": is_authenticated
    }

    return render(request, 'site_admin/festivals.html', context)


def site_admin_festival_images(request):
    is_authenticated = False
    if (request.user.is_authenticated and not request.user.is_superuser and request.user.is_staff):
        is_authenticated = request.user.is_authenticated

    festival_images_dict = defaultdict(list)
    festival_images = FestivalImages.objects.select_related("festival")
    festival_image_form = AdminFestivalImageForm()

    for festival_image in festival_images:
        festival_images_dict[festival_image.festival.name].append(
            festival_image)

    festival_images_dict.default_factory = None

    context = {
        "festival_images": festival_images_dict,
        "form": festival_image_form,
        "is_authenticated": is_authenticated
    }

    return render(request, 'site_admin/festival_images.html', context)


def site_admin_schedule(request):
    is_authenticated = False
    if (request.user.is_authenticated and not request.user.is_superuser and request.user.is_staff):
        is_authenticated = request.user.is_authenticated

    schedule_dict = defaultdict(list)
    schedules = Schedule.objects.select_related('festival')

    for schedule in schedules:
        schedule_dict[schedule.festival.name].append(schedule)

    schedule_dict.default_factory = None
    schedule_form = AdminScheduleForm()
    context = {
        "schedules": schedule_dict,
        "form": schedule_form,
        "is_authenticated": is_authenticated
    }

    return render(request, 'site_admin/schedule.html', context)


def site_admin_dance_performers(request):
    is_authenticated = False
    if (request.user.is_authenticated and not request.user.is_superuser and request.user.is_staff):
        is_authenticated = request.user.is_authenticated

    dancers_dict = defaultdict(list)
    dancers = DancePerformers.objects.select_related("festival")

    for dancer in dancers:
        dancers_dict[dancer.festival.name].append(dancer)

    dancers_dict.default_factory = None

    dancer_form = AdminDancerForm()

    context = {
        "dancers": dancers_dict,
        "form": dancer_form,
        "is_authenticated": is_authenticated
    }

    return render(request, 'site_admin/dance_performers.html', context)


def site_admin_musicians(request):
    is_authenticated = False
    if (request.user.is_authenticated and not request.user.is_superuser and request.user.is_staff):
        is_authenticated = request.user.is_authenticated

    musicians_dict = defaultdict(list)
    musicians = Musicians.objects.select_related("festival")

    for musician in musicians:
        musicians_dict[musician.festival.name].append(musician)

    musicians_dict.default_factory = None

    musician_form = AdminMusicianForm()

    context = {
        "musicians": musicians_dict,
        "form": musician_form,
        "is_authenticated": is_authenticated
    }

    return render(request, 'site_admin/musicians.html', context)


def site_admin_emcees(request):
    is_authenticated = False
    if (request.user.is_authenticated and not request.user.is_superuser and request.user.is_staff):
        is_authenticated = request.user.is_authenticated

    emcees_dict = defaultdict(list)
    emcees = Emcees.objects.select_related("festival")

    for emcee in emcees:
        emcees_dict[emcee.festival.name].append(emcee)

    emcees_dict.default_factory = None

    emcee_form = AdminEmceeForm()

    context = {
        "emcees": emcees_dict,
        "form": emcee_form,
        "is_authenticated": is_authenticated
    }

    return render(request, 'site_admin/emcees.html', context)


def site_admin_food_vendors(request):
    is_authenticated = False
    if (request.user.is_authenticated and not request.user.is_superuser and request.user.is_staff):
        is_authenticated = request.user.is_authenticated

    food_vendors_dict = defaultdict(list)
    food_vendors = FoodVendors.objects.select_related("festival")

    for food_vendor in food_vendors:
        food_vendors_dict[food_vendor.festival.name].append(food_vendor)

    food_vendors_dict.default_factory = None

    food_vendor_form = AdminFoodVendorForm()

    context = {
        "food_vendors": food_vendors_dict,
        "form": food_vendor_form,
        "is_authenticated": is_authenticated
    }

    return render(request, 'site_admin/food_vendors.html', context)


def site_admin_tickets(request):
    is_authenticated = False
    if (request.user.is_authenticated and not request.user.is_superuser and request.user.is_staff):
        is_authenticated = request.user.is_authenticated

    tickets_dict = defaultdict(list)
    tickets = Ticket.objects.select_related("festival")

    for ticket in tickets:
        tickets_dict[ticket.festival.name].append(ticket)

    tickets_dict.default_factory = None

    ticket_form = AdminTicketForm()

    context = {
        "tickets": tickets_dict,
        "form": ticket_form,
        "is_authenticated": is_authenticated
    }

    return render(request, 'site_admin/tickets.html', context)


def site_admin_orders(request):
    is_authenticated = False
    if (request.user.is_authenticated and not request.user.is_superuser and request.user.is_staff):
        is_authenticated = request.user.is_authenticated

    orders_dict = defaultdict(list)
    orders = Order.objects.select_related("user")

    for order in orders:
        orders_dict[order.user.email].append(order)

    orders_dict.default_factory = None

    ticket_form = AdminOrderForm()

    context = {
        "orders": orders_dict,
        "form": ticket_form,
        "is_authenticated": is_authenticated
    }

    return render(request, 'site_admin/orders.html', context)


def site_admin_sponsors(request):
    is_authenticated = False
    if (request.user.is_authenticated and not request.user.is_superuser and request.user.is_staff):
        is_authenticated = request.user.is_authenticated

    sponsors_dict = defaultdict(list)
    sponsors = Sponsor.objects.select_related("festival")

    for sponsor in sponsors:
        sponsors_dict[sponsor.festival].append(sponsor)

    sponsors_dict.default_factory = None

    ticket_form = AdminSponsorForm()

    context = {
        "sponsors": sponsors_dict,
        "form": ticket_form,
        "is_authenticated": is_authenticated
    }

    return render(request, 'site_admin/sponsors.html', context)


def site_admin_volunteers(request):
    is_authenticated = False
    if (request.user.is_authenticated and not request.user.is_superuser and request.user.is_staff):
        is_authenticated = request.user.is_authenticated

    volunteers_dict = defaultdict(list)
    volunteers = Volunteer.objects.select_related("festival")

    for volunteer in volunteers:
        volunteers_dict[volunteer.festival].append(volunteer)

    volunteers_dict.default_factory = None

    volunteer_form = AdminVolunteerForm()

    context = {
        "volunteers": volunteers_dict,
        "form": volunteer_form,
        "is_authenticared": is_authenticated
    }

    return render(request, 'site_admin/volunteers.html', context)


def site_admin_feedbacks(request):
    is_authenticated = False
    if (request.user.is_authenticated and not request.user.is_superuser and request.user.is_staff):
        is_authenticated = request.user.is_authenticated

    feedbacks_dict = defaultdict(list)
    feedbacks = Feedback.objects.select_related("festival")

    for feedback in feedbacks:
        feedbacks_dict[feedback.festival].append(feedback)

    feedbacks_dict.default_factory = None

    feedback_form = AdminFeedbackForm()

    context = {
        "feedbacks": feedbacks_dict,
        "form": feedback_form,
        "is_authenticated": is_authenticated
    }

    return render(request, 'site_admin/feedbacks.html', context)


def create_festival(request):
    if request.POST:
        festival_form = AdminFestivalForm(request.POST, request.FILES)
        if festival_form.is_valid():
            festival_form.save()
            messages.success(request, "You've Sucessfully Created A Festival")
            return redirect(reverse("site_admin_festivals"))
        else:
            return JsonResponse({'errors': festival_form.errors}, status=400)


def create_schedule(request):
    if request.POST:
        schedule_form = AdminScheduleForm(request.POST)
        if schedule_form.is_valid():
            schedule_form.save()
            messages.success(request, "You've Sucessfully Created A Schedule")
            return redirect(reverse("site_admin_schedule"))
        else:
            return JsonResponse({'errors': schedule_form.errors}, status=400)


def create_dance_performer(request):
    if request.POST:
        dancer_form = AdminDancerForm(request.POST, request.FILES)
        if dancer_form.is_valid():
            dancer_form.save()
            messages.success(
                request, "You've Sucessfully Created A Dance Performance")
            return redirect(reverse("site_admin_dance_performers"))
        else:
            return JsonResponse({'errors': dancer_form.errors}, status=400)


def create_musician(request):
    if request.POST:
        musician_form = AdminMusicianForm(request.POST, request.FILES)
        if musician_form.is_valid():
            musician_form.save()
            messages.success(request, "You've Sucessfully Created A Musician")
            return redirect(reverse("site_admin_musicians"))
        else:
            return JsonResponse({'errors': musician_form.errors}, status=400)


def create_emcee(request):
    if request.POST:
        emcee_form = AdminEmceeForm(request.POST, request.FILES)
        if emcee_form.is_valid():
            emcee_form.save()
            messages.success(request, "You've Sucessfully Created An Emcee")
            return redirect(reverse("site_admin_emcees"))
        else:
            return JsonResponse({'errors': emcee_form.errors}, status=400)


def create_food_vendor(request):
    if request.POST:
        food_vendor_form = AdminFoodVendorForm(request.POST, request.FILES)
        if food_vendor_form.is_valid():
            food_vendor_form.save()
            messages.success(
                request, "You've Sucessfully Created A Food Vendor")
            return redirect(reverse("site_admin_food_vendors"))
        else:
            return JsonResponse({'errors': food_vendor_form.errors}, status=400)


def create_ticket(request):
    if request.POST:
        ticket_form = AdminTicketForm(request.POST)
        if ticket_form.is_valid():
            ticket_form.save()
            messages.success(request, "You've Sucessfully Created A Ticket")
            return redirect(reverse("site_admin_tickets"))
        else:
            return JsonResponse({'errors': ticket_form.errors}, status=400)


def create_order(request):
    if request.POST:
        order_form = AdminOrderForm(request.POST)
        if order_form.is_valid():
            order_form.save()
            messages.success(request, "You've Sucessfully Created A Order")
            return redirect(reverse("site_admin_orders"))
        else:
            return JsonResponse({'errors': order_form.errors}, status=400)


def create_sponsor(request):
    if request.POST:
        sponsor_form = AdminSponsorForm(request.POST, request.FILES)
        if sponsor_form.is_valid():
            sponsor_form.save()
            messages.success(request, "You've Sucessfully Created An Sponsor")
            return redirect(reverse("site_admin_sponsors"))
        else:
            return JsonResponse({'errors': sponsor_form.errors}, status=400)


def create_volunteer(request):
    if request.POST:
        volunteer_form = AdminVolunteerForm(request.POST)
        if volunteer_form.is_valid():
            volunteer_form.save()
            messages.success(request, "You've Sucessfully Created A Volunteer")
            return redirect(reverse("site_admin_volunteers"))
        else:
            return JsonResponse({'errors': volunteer_form.errors}, status=400)


def create_feedback(request):
    if request.POST:
        feedback_form = AdminFeedbackForm(request.POST)
        if feedback_form.is_valid():
            feedback_form.save()
            messages.success(request, "You've Sucessfully Created A Feedback")
            return redirect(reverse("site_admin_feedbacks"))
        else:
            return JsonResponse({'errors': feedback_form.errors}, status=400)


def create_festival_image(request):
    if request.POST:
        festival_image_form = AdminFestivalImageForm(
            request.POST, request.FILES)
        if festival_image_form.is_valid():
            festival_image_form.save()
            messages.success(
                request, "You've Sucessfully Created A Festival Image")
            return redirect(reverse("site_admin_festival_images"))
        else:
            return JsonResponse({'errors': festival_image_form.errors}, status=400)


def edit_festival(request, id):
    festival = Festival.objects.get(id=id)
    if request.POST:
        festival_form = AdminFestivalForm(
            request.POST, request.FILES, instance=festival)
        if festival_form.is_valid():
            festival_form.save()
            messages.success(
                request, f"You've Sucessfully Edited {festival.name}!")
            return JsonResponse({"success": True})
        else:
            return JsonResponse({'errors': festival_form.errors}, status=400)
    else:
        festival_json = serializers.serialize(
            "python", [festival], ensure_ascii=False)
        return JsonResponse({"festival": festival_json[0]}, status=200)


def edit_schedule(request, id):
    schedule = Schedule.objects.get(id=id)
    if request.POST:
        schedule_form = AdminScheduleForm(request.POST, instance=schedule)
        if schedule_form.is_valid():
            schedule_form.save()
            messages.success(
                request, f"You've Sucessfully Edited {schedule.act}!")
            return JsonResponse({"success": True})
        else:
            return JsonResponse({'errors': schedule_form.errors}, status=400)
    else:
        schedule_json = serializers.serialize(
            "python", [schedule], ensure_ascii=False)
        return JsonResponse({"schedule": schedule_json[0]}, status=200)


def edit_dance_performer(request, id):
    dancer = DancePerformers.objects.get(id=id)
    if request.POST:
        dancer_form = AdminDancerForm(
            request.POST, request.FILES, instance=dancer)
        if dancer_form.is_valid():
            dancer_form.save()
            messages.success(
                request, f"You've Sucessfully Edited {dancer.name}!")
            return JsonResponse({"success": True})
        else:
            return JsonResponse({'errors': dancer_form.errors}, status=400)
    else:
        festival_json = serializers.serialize(
            "python", [dancer], ensure_ascii=False)
        return JsonResponse({"dancer": festival_json[0]}, status=200)


def edit_musician(request, id):
    musician = Musicians.objects.get(id=id)
    if request.POST:
        musician_form = AdminMusicianForm(
            request.POST, request.FILES, instance=musician)
        if musician_form.is_valid():
            musician_form.save()
            messages.success(
                request, f"You've Sucessfully Edited {musician.name}!")
            return JsonResponse({"success": True})
        else:
            return JsonResponse({'errors': musician_form.errors}, status=400)
    else:
        musicians_json = serializers.serialize(
            "python", [musician], ensure_ascii=False)
        return JsonResponse({"musician": musicians_json[0]}, status=200)


def edit_emcee(request, id):
    emcee = Emcees.objects.get(id=id)
    if request.POST:
        emcee_form = AdminEmceeForm(
            request.POST, request.FILES, instance=emcee)
        if emcee_form.is_valid():
            emcee_form.save()
            messages.success(
                request, f"You've Sucessfully Edited {emcee.name}!")
            return JsonResponse({"success": True})
        else:
            return JsonResponse({'errors': emcee_form.errors}, status=400)
    else:
        emcees_json = serializers.serialize(
            "python", [emcee], ensure_ascii=False)
        return JsonResponse({"emcee": emcees_json[0]}, status=200)


def edit_food_vendor(request, id):
    food_vendor = FoodVendors.objects.get(id=id)
    if request.POST:
        food_vendor_form = AdminEmceeForm(
            request.POST, request.FILES, instance=food_vendor)
        if food_vendor_form.is_valid():
            food_vendor_form.save()
            messages.success(
                request, f"You've Sucessfully Edited {food_vendor.name}!")
            return JsonResponse({"success": True})
        else:
            return JsonResponse({'errors': food_vendor_form.errors}, status=400)
    else:
        food_vendors_json = serializers.serialize(
            "python", [food_vendor], ensure_ascii=False)
        return JsonResponse({"food_vendors": food_vendors_json[0]}, status=200)


def edit_ticket(request, id):
    ticket = Ticket.objects.get(id=id)
    if request.POST:
        ticket_form = AdminTicketForm(request.POST, instance=ticket)
        if ticket_form.is_valid():
            ticket_form.save()
            messages.success(
                request, f"You've Sucessfully Edited {ticket.ticket_type}!")
            return JsonResponse({"success": True})
        else:
            return JsonResponse({'errors': ticket_form.errors}, status=400)
    else:
        tickets_json = serializers.serialize(
            "python", [ticket], ensure_ascii=False)
        return JsonResponse({"ticket": tickets_json[0]}, status=200)


def edit_order(request, id):
    order = Order.objects.get(id=id)
    if request.POST:
        order_form = AdminOrderForm(request.POST, instance=order)
        if order_form.is_valid():
            order_form.save()
            messages.success(
                request, f"You've Sucessfully Edited {order.order_name}!")
            return JsonResponse({"success": True})
        else:
            return JsonResponse({'errors': order_form.errors}, status=400)
    else:
        orders_json = serializers.serialize(
            "python", [order], ensure_ascii=False)
        return JsonResponse({"order": orders_json[0]}, status=200)


def edit_sponsor(request, id):
    sponsor = Sponsor.objects.get(id=id)
    if request.POST:
        sponsor_form = AdminSponsorForm(
            request.POST, request.FILES, instance=sponsor)
        if sponsor_form.is_valid():
            sponsor_form.save()
            messages.success(
                request, f"You've Sucessfully Edited {sponsor.email}!")
            return JsonResponse({"success": True})
        else:
            return JsonResponse({'errors': sponsor_form.errors}, status=400)
    else:
        sponsors_json = serializers.serialize(
            "python", [sponsor], ensure_ascii=False)
        return JsonResponse({"sponsor": sponsors_json[0]}, status=200)


def edit_volunteer(request, id):
    volunteer = Volunteer.objects.get(id=id)
    if request.POST:
        volunteer_form = AdminVolunteerForm(
            request.POST, request.FILES, instance=volunteer)
        if volunteer_form.is_valid():
            volunteer_form.save()
            messages.success(
                request, f"You've Sucessfully Edited {volunteer.email}!")
            return JsonResponse({"success": True})
        else:
            return JsonResponse({'errors': volunteer_form.errors}, status=400)
    else:
        volunteers_json = serializers.serialize(
            "python", [volunteer], ensure_ascii=False)
        return JsonResponse({"volunteer": volunteers_json[0]}, status=200)


def edit_feedback(request, id):
    feedback = Feedback.objects.get(id=id)
    if request.POST:
        feedback_form = AdminFeedbackForm(request.POST, instance=feedback)
        if feedback_form.is_valid():
            feedback_form.save()
            messages.success(
                request, f"You've Sucessfully Edited {feedback.first_name} {feedback.last_name}!")
            return JsonResponse({"success": True})
        else:
            return JsonResponse({'errors': feedback_form.errors}, status=400)
    else:
        feedbacks_json = serializers.serialize(
            "python", [feedback], ensure_ascii=False)
        return JsonResponse({"feedback": feedbacks_json[0]}, status=200)


def edit_festival_image(request, id):
    festival_image = FestivalImages.objects.get(id=id)
    if request.POST:
        festival_image_form = AdminFestivalImageForm(
            request.POST, request.FILES, instance=festival_image)
        if festival_image_form.is_valid():
            festival_image_form.save()
            messages.success(
                request, f"You've Sucessfully Edited {festival_image.image_title}!")
            return JsonResponse({"success": True})
        else:
            return JsonResponse({'errors': festival_image_form.errors}, status=400)
    else:
        festival_image_json = serializers.serialize(
            "python", [festival_image], ensure_ascii=False)
        return JsonResponse({"festival_image": festival_image_json[0]}, status=200)


@require_http_methods(["DELETE"])
@csrf_exempt
def delete_festival(request, id):
    try:
        festival = Festival.objects.get(id=id)
        festival.delete()
        messages.success(request, f"{festival.name}, sucessfully deleted!")
        return JsonResponse({"success": True})
    except:
        return JsonResponse({"error": "Not Found"}, status=404)


@require_http_methods(["DELETE"])
@csrf_exempt
def delete_schedule(request, id):
    try:
        schedule = Schedule.objects.get(id=id)
        schedule.delete()
        messages.success(request, f"{schedule.act}, sucessfully deleted!")
        return JsonResponse({"success": True})
    except:
        return redirect(reverse("error", kwargs={"code": 401}))


@require_http_methods(["DELETE"])
@csrf_exempt
def delete_dance_performer(request, id):
    try:
        dancer = DancePerformers.objects.get(id=id)
        dancer.delete()
        messages.success(request, f"{dancer.name}, sucessfully deleted!")
        return JsonResponse({"success": True})
    except Exception as e:
        return redirect(reverse("error", kwargs={"code": 401}))


@require_http_methods(["DELETE"])
@csrf_exempt
def delete_musician(request, id):
    try:
        musician = Musicians.objects.get(id=id)
        musician.delete()
        messages.success(request, f"{musician.name}, sucessfully deleted!")
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"error": "Not Found"}, status=404)


@require_http_methods(["DELETE"])
@csrf_exempt
def delete_emcee(request, id):
    try:
        emcee = Emcees.objects.get(id=id)
        emcee.delete()
        messages.success(request, f"{emcee.name}, sucessfully deleted!")
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"error": "Not Allowd"}, status=405)


@require_http_methods(["DELETE"])
@csrf_exempt
def delete_food_vendor(request, id):
    try:
        food_vendor = FoodVendors.objects.get(id=id)
        food_vendor.delete()
        messages.success(request, f"{food_vendor.name}, sucessfully deleted!")
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"error": "Not Found"}, status=404)


@require_http_methods(["DELETE"])
@csrf_exempt
def delete_ticket(request, id):
    try:
        ticket = Ticket.objects.get(id=id)
        ticket.delete()
        messages.success(
            request, f"{ticket.ticket_type}, sucessfully deleted!")
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"error": "Not Found"}, status=404)


@require_http_methods(["DELETE"])
@csrf_exempt
def delete_order(request, id):
    try:
        order = Order.objects.get(id=id)
        order.delete()
        messages.success(request, f"{order.order_name}, sucessfully deleted!")
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"error": "Not Found"}, status=404)


@require_http_methods(["DELETE"])
@csrf_exempt
def delete_sponsor(request, id):
    try:
        sponsor = Sponsor.objects.get(id=id)
        sponsor.delete()
        messages.success(request, f"{sponsor.email}, sucessfully deleted!")
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"error": "Not Found"}, status=404)


@require_http_methods(["DELETE"])
@csrf_exempt
def delete_volunteer(request, id):
    try:
        volunteer = Volunteer.objects.get(id=id)
        volunteer.delete()
        messages.success(request, f"{volunteer.email}, sucessfully deleted!")
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"error": "Not Found"}, status=404)


@require_http_methods(["DELETE"])
@csrf_exempt
def delete_feedback(request, id):
    try:
        feedback = Feedback.objects.get(id=id)
        feedback.delete()
        messages.success(
            request, f"{feedback.first_name} {feedback.last_name}, sucessfully deleted!")
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"error": "Not Found"}, status=404)


@require_http_methods(["DELETE"])
@csrf_exempt
def delete_festival_image(request, id):
    try:
        festival_image = FestivalImages.objects.get(id=id)
        festival_image.delete()
        messages.success(
            request, f"{festival_image.image_title}, sucessfully deleted!")
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"error": "Not Found"}, status=404)
