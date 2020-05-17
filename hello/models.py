from django.db import models
from django.contrib.auth.models import User
from django import forms 



# Create your models here.
class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)
    
    def __str__(self):
        return f"{self.city}"


class Flight(models.Model):
    id = models.CharField(max_length=3, primary_key=True)
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="destination")
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.origin} - {self.destination}"

class Passenger(models.Model):
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    flights = models.ManyToManyField(Flight, blank=True, related_name="passengers")

    def __str__(self):
        return f"{self.first}"

class Profile(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   first = models.CharField(max_length=20, blank=True)
   last = models.CharField(max_length=20, blank=True)
   bio = models.CharField(blank=True, max_length=2000)
   birthdate = models.DateField(blank=True)
   friendRequests = models.ManyToManyField(User, related_name="requests", null=True)
   friends = models.ManyToManyField(User, related_name="friends", null=True)




