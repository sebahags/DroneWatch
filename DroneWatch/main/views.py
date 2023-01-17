from django.shortcuts import render
from django.http import HttpResponse
from .models import DroneInfo, Scraper, CalculateDistance

# Create your views here.

def index(response):
    Scraper()
    all_drones = DroneInfo.objects.all()
    context = {
        'all_drones' : all_drones,
        
    }
    return render(response, "main/index.html", context)