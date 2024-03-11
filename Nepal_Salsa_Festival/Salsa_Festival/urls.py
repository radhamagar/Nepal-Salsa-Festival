from django.urls import path, include
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('contact', views.contact, name='contact'),
    path('schedule', views.schedule, name='schedule'),
    path('about', views.about, name='about'),
    path('tickets/<int:id>/', views.tickets, name='tickets'),
    path('payment/<int:id>/', views.payment, name='payment'),
    path('khalti_gateway', views.khalti_gateway, name='khalti_gateway'),
    path('', include('authentication.urls')),
    path('', include('festivals.urls')),
]
