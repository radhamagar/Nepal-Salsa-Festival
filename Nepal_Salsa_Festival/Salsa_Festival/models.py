from django.db import models
from festivals.models import Festival

class Volunteer(models.Model):
    festival = models.ForeignKey(Festival, on_delete=models.CASCADE)
    email = models.CharField(max_length=255)
    ph_number = models.CharField(max_length=10)

    def __str__(self):
        return self.email

class Sponsor(models.Model):
    festival = models.ForeignKey(Festival, on_delete=models.CASCADE)
    email = models.CharField(max_length=255)
    ph_number = models.CharField(max_length=10)

    def __str__(self):
        return self.email

