from django.urls import path
from . import views

urlpatterns = [
    path('site_admin', view=views.site_admin, name="site_admin"),
]
