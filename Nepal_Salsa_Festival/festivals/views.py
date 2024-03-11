from django.shortcuts import render, redirect
from .forms import FestivalForm
from datetime import datetime, date
from .models import *
from django.forms import modelformset_factory
import json
import requests
from django.http import HttpResponse

# Create your views here.
def festivals(request):
    image_form_set = modelformset_factory(model=Festival, form=FestivalForm, extra=10)

#    if (request.method == "POST"):
#        festival_form = FestivalForm(request.POST)
#        form_set = image_form_set(request.POST, request.FILES, queryset=FestivalImages.objects.none())
#
#        if (festival_form.is_valid() and form_set.is_valid()):
#            festival_form = festival_form.save(commit=False)
#            festival_form.user = request.user
#            festival_form.save()
#
#            for form in form_set.cleaned_data:
#                if form:
#                    image = form["image"]
#                    photo = FestivalImages(festival_form, image)
#                    photo.save()
#            return redirect("/")
#        else:
#            print(festival_form.errors, formset.errors)

    festival_images = {}

    festivals = Festival.objects.all()

    for festival in festivals:
        if(datetime.strptime(festival.date_time.strftime('%Y-%m-%d'), '%Y-%m-%d').date() < date.today()):
            image = festival.feature_image
            festival_images[festival.name] = {
                    "image" : image,
                    "id" : festival.id,
            }

    dance_performances = DancePerformers.objects.filter(festival__date_time__lt=datetime.now()).distinct()
    musicians = Musicians.objects.filter(festival__date_time__lt=datetime.now()).distinct()
    food_vendors = FoodVendors.objects.filter(festival__date_time__lt=datetime.now()).distinct()
    emcees = Emcees.objects.filter(festival__date_time__lt=datetime.now()).distinct()

    context = {
        "festival_images" : festival_images,
        "dance_performances" : dance_performances,
        "musicians" : musicians,
        "food_vendors" : food_vendors,
        "emcees" : emcees
    }

    return render(request, "festivals/festivals.html",context)

def festival_description(request, id):
    festival = Festival.objects.get(id=id)
    images = FestivalImages.objects.filter(festival__id=id)

    context = {
        "festival" : festival,
        "images" : images
    }
    return render(request, "festivals/festival_description.html", context)

def success(request):
    context = {}
    return render(request, "success.html", context)

