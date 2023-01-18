from django.shortcuts import render
from .models import DroneInfo, Scraper




def index(response):
    #delete instances older than 10 min
    DroneInfo.DeleteOlds()
    #get all instances for the context
    all_drones = DroneInfo.objects.all()
    #call the Scraper function from models        
    Scraper()
    context = {
        'all_drones' : all_drones,    
    }
    return render(response, "main/index.html", context)