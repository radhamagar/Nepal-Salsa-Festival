from django.urls import path
from . import views

urlpatterns = [
        path("broadcaster/", views.broadcaster, name="broadcaster"),
        path("viewer/", views.viewer, name="viewer"),

        path("broadcast/", views.broadcast, name="broadcast"),
        path("consumer/", views.consumer, name="consumer"),

        path('offer/', views.offer, name='offer'),
        path('answer/', views.answer, name='answer'),
        path('get_offer/', views.get_offer, name='get_offer'),
        path('get_answer/', views.get_answer, name='get_answer'),
]
