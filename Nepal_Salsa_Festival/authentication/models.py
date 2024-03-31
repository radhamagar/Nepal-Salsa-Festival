from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from .managers import SiteUserManager
from django.core.validators import RegexValidator
import re

phone_validator = RegexValidator(
    regex=r"(\+977)?[9][6-9]\d{8}",
    message="Phone number must be in the form: 9800000000"
)

# Create your models here.
class SiteUser(AbstractUser):
    ph_number = models.CharField(max_length=20, validators=[phone_validator])
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100,unique=False, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = SiteUserManager()

    def __str__(self):
        return self.email

