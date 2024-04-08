from django.urls import path
from . import views

urlpatterns = [
        path("live/", views.live, name="live"),
        path("lobby/", views.lobby, name="lobby"),
]
