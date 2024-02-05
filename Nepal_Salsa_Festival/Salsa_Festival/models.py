from django.db import models

class Home(models.Model):
    home_img = models.ImageField(upload_to="images/")
    home_description = models.CharField(max_length=200)