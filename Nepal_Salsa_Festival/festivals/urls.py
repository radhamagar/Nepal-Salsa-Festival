from django.urls import path
from . import views

urlpatterns = [
    path(route='festivals', view=views.festivals, name='festivals'),
    path(route='festivals/<int:id>', view=views.festival_description, name='festival_description'),
    path(route='success', view=views.success, name='success'),
]
