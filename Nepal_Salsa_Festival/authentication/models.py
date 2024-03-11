from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from .managers import SiteUserManager

# Create your models here.
class SiteUser(AbstractUser):
    ph_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100,unique=False, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = SiteUserManager()

    def __str__(self):
        return self.email
