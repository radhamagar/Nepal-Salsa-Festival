from django.shortcuts import render

# Create your views here.
def live(request):
    room_id = request.GET.get('room')
    context = {}

    return render(request, "live_streaming/live.html", context)


def lobby(request):
    context = {}

    return render(request, "live_streaming/lobby.html", context)
