from django.db import models
import math
from bs4 import BeautifulSoup
import requests
import json

# Create your models here.

class DroneInfo(models.Model):
    serialNumber = models.CharField(max_length=20)
    positionY = models.FloatField()
    positionX = models.FloatField()
    distanceNest = models.FloatField()
    pilotFirstName = models.CharField(max_length=50)
    pilotLastName = models.CharField(max_length=50)
    pilotMail = models.CharField(max_length=50)
    pilotPhone = models.CharField(max_length=20)

    def __str__(self):
        return self.serialNumber
    
    


def CalculateDistance(x, y):
        nestX = float(250000)
        nestY = float(250000)
        positionX = x
        positionY = y
        if positionX > nestX and positionY > nestY:
            return math.sqrt((math.pow((positionX - nestX), 2) + math.pow((positionY - nestY), 2)))
        elif positionX > nestX and positionY < nestY:
            return math.sqrt((math.pow((positionX - nestX), 2) + math.pow((nestY - positionY), 2)))
        elif positionX < nestX and positionY > nestY:
            return math.sqrt((math.pow((nestX - positionX), 2) + math.pow((positionY - nestY), 2)))
        else:
            return math.sqrt((math.pow((nestX - positionX), 2) + math.pow((nestY - positionY), 2)))
    
def Scraper():
        url = "https://assignments.reaktor.com/birdnest/drones"
        xml = requests.get(url)
        soup = BeautifulSoup(xml.content, 'xml')
        for item in soup.findAll('drone'):
            serialNumber = str(item.find('serialNumber').text)
            positionx = float(item.find('positionX').text)
            positiony = float(item.find('positionY').text)
            if CalculateDistance(positionx, positiony) < float(100000):
                url_person = f"https://assignments.reaktor.com/birdnest/pilots/{serialNumber}"
                jason = requests.get(url_person)
                jason_soup = BeautifulSoup(jason.content, 'lxml')
                json1 = json.loads(jason_soup.string)
                firstName = json1.get('firstName')
                lastName = json1.get('lastName')
                email = json1.get('email')
                phoneNumber = json1.get('phoneNumber')
                drone = DroneInfo(pilotFirstName=firstName, pilotLastName=lastName, serialNumber=serialNumber, pilotPhone=phoneNumber, pilotMail=email, distanceNest=CalculateDistance(positionx, positiony), positionY=positiony, positionX=positionx)
                drone.save()
                