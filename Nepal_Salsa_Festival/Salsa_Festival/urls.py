from django.urls import path, include
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('participate/', views.participate, name='participate'),
    path('schedule/', views.schedule, name='schedule'),
    path('events/', views.events, name='events'),
    path('about/', views.about, name='about'),
    path('feedback/', views.feedback, name='feedback'),
    path('tickets/<int:id>/', views.tickets, name='tickets'),
    path('payment/<int:id>/', views.payment, name='payment'),
    path('khalti_gateway/<int:id>', views.khalti_gateway, name='khalti_gateway'),
    path('', include('authentication.urls')),
    path('', include('festivals.urls')),
    path('', include('site_admin.urls')),
    path('', include('live_streaming.urls')),
]
