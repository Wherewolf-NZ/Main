from django.shortcuts import render
from app_main.models import *

# Create your views here.
def admin_home(request):

    features = Feature.objects.latest()

    render(request, "home.html")