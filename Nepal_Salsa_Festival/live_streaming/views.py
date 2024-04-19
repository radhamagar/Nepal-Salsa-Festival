from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from aiortc import *
import asyncio
import json
from django.core.serializers.json import DjangoJSONEncoder

servers = RTCIceServer("stun:stun.stunprotocol.org")
configuration = RTCConfiguration([servers])
sender_stream = None
track_to_stream = {}

# Define the Stream class
class Stream:
    def __init__(self):
        self.tracks = []

    def addTrack(self, track):
        self.tracks.append(track)

    def getTracks(self):
        return self.tracks

# Create your views here.
def broadcaster(request):
    context = {}

    return render(request, "live_streaming/broadcast.html", context)


def viewer(request):
    context = {}

    return render(request, "live_streaming/viewer.html", context)

@csrf_exempt
async def consumer(request):
    global sender_stream, track_to_stream
    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)

            sdp_type = body_data['sdp']['type']
            sdp_description = body_data['sdp']['sdp']

            peer = RTCPeerConnection(configuration)

            # Set remote description
            remote_desc = RTCSessionDescription(sdp_description, sdp_type)
            await peer.setRemoteDescription(remote_desc)

            tracks = sender_stream.getTracks()

            for track in tracks:
                peer.addTrack(track);

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

        peer = RTCPeerConnection(configuration)

        async def on_track(track):
            global sender_stream
            sender_stream = track_to_stream.get(track.id, None)
            if sender_stream is None:
                sender_stream = Stream()
                sender_stream.addTrack(track)
                track_to_stream[track.id] = sender_stream

        peer.on('track', on_track)

        await peer.setRemoteDescription(RTCSessionDescription(sdp_description, sdp_type))
        answer = await peer.createAnswer()
        await peer.setLocalDescription(answer)

        payload = {
                'type': peer.localDescription.type,
                'sdp': peer.localDescription.sdp
        }

        return JsonResponse(payload, encoder=DjangoJSONEncoder)
