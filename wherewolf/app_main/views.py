from django.shortcuts import render, redirect
from app_main.models import *


def redirect_to_home(request):
    return redirect("/home/")


def main_home(request):

    features = Feature.objects.get_latest()
    contextData = {
        'features': features
    }

    return render(request, "html/page-home.html", contextData)
