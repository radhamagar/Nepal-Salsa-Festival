from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    ph_number = models.CharField(max_length=20)
    password = models.CharField(max_length=200)
    c_password = models.CharField(max_length=200)
