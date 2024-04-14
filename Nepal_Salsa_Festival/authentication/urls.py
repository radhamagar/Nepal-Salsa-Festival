from django.urls import path
from . import views

urlpatterns = [
    path(route='signin', view=views.signin, name="signin"),
    path(route='signup', view=views.signup, name="signup"),
    path(route='logout/', view=views.logout_view, name="logout"),
    path(route='lost_password/', view=views.lost_password, name="lost_password"),
    path(route='profile/', view=views.profile, name="profile"),
]
