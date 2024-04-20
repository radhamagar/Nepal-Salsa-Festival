from django.shortcuts import render
from django.http import HttpResponse
from festivals.models import Order, TicketAmount
from django.contrib import messages
from django.shortcuts import redirect, reverse
# Create your views here.


def broadcaster(request):
    is_authenticated = False
    if (request.user.is_authenticated and request.user.is_staff):
        is_authenticated = request.user.is_authenticated
    else:
        return HttpResponse("Not Authenticated", 403)

    context = {
        "is_authenticated": is_authenticated
    }
    return render(request, "live_streaming/broadcast.html", context)


def viewer(request):
    user = request.user
    orders = Order.objects.filter(user_id=user.id)
    has_access = False
    is_authenticated = False
    if (request.user.is_authenticated and not request.user.is_staff and not request.user.is_superuser):
        is_authenticated = request.user.is_authenticated

    if not is_authenticated:
        messages.error(request, "Please Log In, Before Accessing the Live Stream")
        return redirect(reverse("signin"))

    try:
        room_id = int(request.GET["room"])

        for order in orders:
            if ((order.lobby_id != 0) and (order.lobby_id == room_id)):
                has_access = True
                break
        if (not has_access):
            messages.error(request, "Please Enter a Valid Room Id.")
            return redirect(reverse("lobby"))

    except Exception:
        messages.error(request, "Please Enter a Room Id.")
        return redirect(reverse("lobby"))
    context = {
            "is_authenticated": is_authenticated
        }

    return render(request, "live_streaming/viewer.html", context)


def lobby(request):
    is_authenticated = False
    if (request.user.is_authenticated and not request.user.is_staff and not request.user.is_superuser):
        is_authenticated = request.user.is_authenticated
    else:
        return HttpResponse("Not Authenticated", 403)

    context = {
        "is_authenticated": is_authenticated
    }
    return render(request, "live_streaming/lobby.html", context)
