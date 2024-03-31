from django.db import models
from authentication.models import SiteUser
from django.utils.text import slugify

# Create your models here.
def get_image_file(instance, filename):
    title = instance.festival.name
    slug = slugify(title)
    return "uploads/%s-%s" % (slug, filename)

class Festival(models.Model):
    user = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date_time = models.DateTimeField()
    description = models.CharField(max_length=1000)
    past_description = models.CharField(max_length=1000, blank=True, null=True)
    feature_image = models.ImageField(upload_to=f'uploads/{slugify(name)}', verbose_name="Festival", null=True)
    location = models.CharField(max_length=255, null=True)
    is_next = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class FestivalImages(models.Model):
    festival = models.ForeignKey(Festival, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_file, verbose_name="Image")
    image_title = models.CharField(max_length=255, name=image.name, null="True")

    def __str__(self):
        return self.image_title

class DancePerformers(models.Model):
    festival = models.ForeignKey(Festival, default=None, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    act = models.CharField(max_length=255)
    image = models.ImageField(upload_to=get_image_file, verbose_name="Dance Image", null="True")

    def __str__(self):
        return self.name

class Musicians(models.Model):
    festival = models.ForeignKey(Festival, default=None, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    act = models.CharField(max_length=255)
    image = models.ImageField(upload_to=get_image_file, verbose_name="Musicians", null="True")

    def __str__(self):
        return self.name

class Emcees(models.Model):
    festival = models.ForeignKey(Festival, default=None, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=get_image_file, verbose_name="Emcees", null="True")

    def __str__(self):
        return self.name

class FoodVendors(models.Model):
    festival = models.ForeignKey(Festival, default=None, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=get_image_file, verbose_name="FoodVendors", null="True")

    def __str__(self):
        return self.name

class Ticket(models.Model):
    festival = models.ForeignKey(to=Festival, on_delete=models.CASCADE)
    ticket_type = models.CharField(max_length=255, default="Regular")
    price = models.PositiveIntegerField(default=0)
    max_amount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.festival.user.first_name

class TicketAmount(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.ticket.ticket_type

class Order(models.Model):
    user = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    ticket_amounts = models.ManyToManyField(to=TicketAmount, related_name="orders")

    def __str__(self):
        return self.user.email;
