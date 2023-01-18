from django.db import models
import math
from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime, timezone

#creates a model to the database
class DroneInfo(models.Model):
    serialNumber = models.CharField(max_length=20)
    positionY = models.FloatField()
    positionX = models.FloatField()
    distanceNest = models.FloatField()
    pilotFirstName = models.CharField(max_length=50)
    pilotLastName = models.CharField(max_length=50)
    pilotMail = models.CharField(max_length=50)
    pilotPhone = models.CharField(max_length=20)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.serialNumber
    # deleting the instances of the class DroneInfo that are older than 600 sec
    def DeleteOlds():
        all_drones = DroneInfo.objects.all()
        now = datetime.now(timezone.utc)
        for i in all_drones:
            deltaTime = now - i.date_added
            if deltaTime.seconds > 600:
                i.delete()


# Function to calculate the distance from the nest, 4 different sections of the round area        
def CalculateDistance(x, y):
        nestX = float(250000)
        nestY = float(250000)
        positionX = x
        positionY = y
        if positionX > nestX and positionY > nestY:
            return (math.sqrt((math.pow((positionX - nestX), 2) + math.pow((positionY - nestY), 2))))/1000
        elif positionX > nestX and positionY < nestY:
            return (math.sqrt((math.pow((positionX - nestX), 2) + math.pow((nestY - positionY), 2))))/1000
        elif positionX < nestX and positionY > nestY:
            return (math.sqrt((math.pow((nestX - positionX), 2) + math.pow((positionY - nestY), 2))))/1000
        else:
            return (math.sqrt((math.pow((nestX - positionX), 2) + math.pow((nestY - positionY), 2))))/1000

            
# Function to scrape and parse the data, also creates a new instance of DroneInfo to the database if needed
# If there is already a instance in the database with a matching serialnumber, then the old instance will be edited    
def Scraper():
        url = "https://assignments.reaktor.com/birdnest/drones"
        xml = requests.get(url)
        soup = BeautifulSoup(xml.content, 'xml')
        
        for item in soup.findAll('drone'):
            newSerialNumber = str(item.find('serialNumber').text)
            positionx = float(item.find('positionX').text)
            positiony = float(item.find('positionY').text)
            if CalculateDistance(positionx, positiony) < float(100):
                url_person = f"https://assignments.reaktor.com/birdnest/pilots/{newSerialNumber}"
                jason = requests.get(url_person)
                jason_soup = BeautifulSoup(jason.content, 'lxml')
                json1 = json.loads(jason_soup.string)
                firstName = json1.get('firstName')
                lastName = json1.get('lastName')
                email = json1.get('email')
                phoneNumber = json1.get('phoneNumber')
                existing_drones = DroneInfo.objects.filter(serialNumber=newSerialNumber)
                if existing_drones.exists():
                    instanceDrone=DroneInfo.objects.get(serialNumber=newSerialNumber)
                    if CalculateDistance(positionx, positiony) < instanceDrone.distanceNest:
                            instanceDrone.distanceNest = CalculateDistance(positionx, positiony)
                    else:
                        pass
                    instanceDrone.date_added = datetime.now(timezone.utc)
                    instanceDrone.save()
                else:
                    drone = DroneInfo(pilotFirstName=firstName, pilotLastName=lastName, serialNumber=newSerialNumber, pilotPhone=phoneNumber, pilotMail=email, distanceNest=CalculateDistance(positionx, positiony), positionY=positiony, positionX=positionx)
                    drone.save()

                

                
                