from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from aiortc import RTCPeerConnection, RTCSessionDescription
import asyncio
import json
from django.core.serializers.json import DjangoJSONEncoder

# Define the Stream class
class Stream:
    def __init__(self):
        self.tracks = []

    def addTrack(self, track):
        self.tracks.append(track)

# Create your views here.
def broadcaster(request):
    context = {}

    return render(request, "live_streaming/broadcast.html", context)


def viewer(request):
    context = {}

    return render(request, "live_streaming/viewer.html", context)

sender_stream = None
track_to_stream = {}

@csrf_exempt
async def consumer(request):
    global sender_stream, track_to_stream
    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)

            sdp_type = body_data['sdp']['type']
            sdp_description = body_data['sdp']['sdp']

            peer = RTCPeerConnection()

            async def on_track(track):
                sender_stream
                sender_stream = track_to_stream.get(track.id, None)
                if sender_stream is None:
                    sender_stream = Stream()
                    track_to_stream[track.id] = sender_stream
                sender_stream.addTrack(track)

            peer.on('track', on_track)

            # Set remote description
            remote_desc = RTCSessionDescription(sdp_description, sdp_type)
            await peer.setRemoteDescription(remote_desc)

            # Generate answer
            answer = await peer.createAnswer()
            await peer.setLocalDescription(answer)

            # Send answer back to remote peer
            sdp_json = {
                'type': peer.localDescription.type,
                'sdp': peer.localDescription.sdp
            }
            return JsonResponse({'sdp': sdp_json}, encoder=DjangoJSONEncoder)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
async def broadcast(request):
    global sender_stream
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)

        sdp_type = body_data['sdp']['type']
        sdp_description = body_data['sdp']['sdp']

        peer = RTCPeerConnection()

        async def on_track(track):
            global sender_stream
            sender_stream = track_to_stream.get(track.id, None)
            if sender_stream is None:
                sender_stream = Stream()
                track_to_stream[track.id] = sender_stream
            sender_stream.addTrack(track)

        peer.on('track', on_track)
        await peer.setRemoteDescription(RTCSessionDescription(sdp_description, sdp_type))
        answer = await peer.createAnswer()
        await peer.setLocalDescription(answer)

        sdp_json = {
            'type': peer.localDescription.type,
            'sdp': peer.localDescription.sdp
        }

        return JsonResponse({'sdp': sdp_json}, encoder=DjangoJSONEncoder)

data = {}

def offer(request):
    if request.method == 'POST':
        offer_data = json.loads(request.body)
        if offer_data.get("type") == "offer":
            data["offer"] = offer_data
            return JsonResponse({}, status=200)
    return HttpResponseBadRequest()

def answer(request):
    if request.method == 'POST':
        answer_data = json.loads(request.body)
        if answer_data.get("type") == "answer":
            data["answer"] = answer_data
            return JsonResponse({}, status=200)
    return HttpResponseBadRequest()

def get_offer(request):
    if "offer" in data:
        offer = data.pop("offer")
        return JsonResponse(offer, status=200)
    else:
        return HttpResponseServerError()

def get_answer(request):
    if "answer" in data:
        answer = data.pop("answer")
        return JsonResponse(answer, status=200)
    else:
        return HttpResponseServerError()
