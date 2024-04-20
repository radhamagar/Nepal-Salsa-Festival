from django.urls import path
from . import views

urlpatterns = [
        path("broadcaster/", views.broadcaster, name="broadcaster"),
        path("viewer/", views.viewer, name="viewer"),
        path("lobby/", views.lobby, name="lobby"),
]
