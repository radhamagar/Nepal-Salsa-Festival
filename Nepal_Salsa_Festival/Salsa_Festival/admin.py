from django.contrib import admin
from festivals.models import *

# Register your models here.
class SiteAdmin(admin.AdminSite):
    site_header = "Nepal Salsa Festival | Admin"

site_admin = SiteAdmin(name="SiteAdmin")

site_admin.register(Festival)
site_admin.register(Schedule)
site_admin.register(FestivalImages)
site_admin.register(FoodVendors)
site_admin.register(Emcees)
site_admin.register(DancePerformers)
site_admin.register(Musicians)
site_admin.register(Ticket)
site_admin.register(Order)


admin.site.register(Festival)
admin.site.register(Schedule)
admin.site.register(FestivalImages)
admin.site.register(FoodVendors)
admin.site.register(Emcees)
admin.site.register(DancePerformers)
admin.site.register(Musicians)
admin.site.register(Ticket)
admin.site.register(Order)
