from django.shortcuts import render

# Create your views here.
def site_admin(request):
    context = {}
    return render(request, 'site_admin/login.html', context)
