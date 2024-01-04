from django.db import models

class Register(models.Model):
      first_name = models.CharField(max_length=100)
      last_name = models.CharField( max_length=100)
      email = models.CharField(max_length=100)
      password=models.CharField(max_length=100)
      confirm_password=models.CharField(max_length=100)
      ph_no=models.IntegerField()
        
