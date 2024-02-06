from django.urls import path
from . import views

urlpatterns = [
    path(route='signin', view=views.signin, name="signin"),
    path(route='signup', view=views.signup, name="signup"),
]
