from django.db import models
from festivals.models import Festival
from django.utils.text import slugify

class Volunteer(models.Model):
    festival = models.ForeignKey(Festival, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255, unique=True)
    ph_number = models.CharField(max_length=10)

    def __str__(self):
        return self.email

class Sponsor(models.Model):
    festival = models.ForeignKey(Festival, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    ph_number = models.CharField(max_length=10)
    feature_image = models.ImageField(upload_to=f"uploads/{slugify(name)}")

    def __str__(self):
        return self.email

class Feedback(models.Model):
    festival = models.ForeignKey(Festival, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

