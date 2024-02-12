from django.urls import path, include
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('contact', views.contact, name='contact'),
    path('schedule', views.schedule, name='schedule'),
    path('', include('authentication.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
