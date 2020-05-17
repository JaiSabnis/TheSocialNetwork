from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from .models import Flight, Passenger, Profile
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError



def accept(request, user_id):
    try:    
        myprofile = Profile.objects.get(user_id=request.user.id)
        friend = User.objects.get(id=user_id)
        myprofile.friends.add(friend)        
        myprofile.friendRequests.remove(friend)
        myprofile.save()
    except Profile.DoesNotExist:
        raise Http404("You haent made a profile yet.")
    context={
            "friend": friend
        }
    return render(request, "flights/accept.html", context)



def register_view(request):
    if request.method == 'GET':
        return render(request, "flights/register.html", {"message":None})
    
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        
        try:
            user = User.objects.create_user(
                username = request.POST["username"],
                email = request.POST["email"],
                password = request.POST["password"])
            user.save()
        except IntegrityError:
            return render(request, "flights/register.html", {"message": "Username already exists"})
        

        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "flights/register.html", {"message": "invalid credentials"})


# Create your views here.

def profile(request, user_id):    
    if request.method == 'POST':
        try:    
            profile = Profile.objects.get(user_id=user_id)
            user = User.objects.get(id=user_id)
            profile.friendRequests.add(request.user)
            profile.save()
        except Profile.DoesNotExist:
            raise Http404("This user hasn't made a profile yet.")
        context={
                "user": user,
                "requested": "requested"
            }
        return render(request, "flights/friendRequest.html", context)

    if request.method == 'GET':      
        try:
            profile = Profile.objects.get(user_id=user_id)
            friends = profile.friends.all()
            requests = profile.friendRequests.all()
            user = User.objects.get(id=user_id)
        except Profile.DoesNotExist:    
            raise Http404("This user hasn't made a profile yet.")

        if request.user in friends:
            context={
                "username": user.username, 
                "first": profile.first,
                "last": profile.last,
                "bio": profile.bio,
                "date": profile.birthdate
            }
            return render(request, "flights/profileDisplay.html", context)  
        elif request.user in requests:
            context={
                "user": user,
                "requested": "requested"
            }
            return render(request, "flights/friendRequest.html", context)
        else:
            context={
                "user": user,
                "notRequested": "not"
            }
            return render(request, "flights/friendRequest.html", context)


def index(request):
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user_id=request.user.id)
            requests = profile.friendRequests.all()
        except Profile.DoesNotExist:
            context = {
                    "username": "Create a profile",
                    "first": "You may choose to enter your first name",
                    "last": "You may choose to enter your first name",
                    "bio": "You may choose to enter your bio",
                    "date": "You must be above the age of 16 to register for this site"}
            return render(request, "flights/profileCreate.html", context)

    if request.method == 'GET':
        if not request.user.is_authenticated:
            return render(request, "flights/login.html", {"message": None})
        context = {
            "users": None,
            "profile": Profile.objects.get(user_id=request.user.id),
            "requests": requests
        }
        return render(request, "flights/index.html", context)
        
    if request.method == 'POST':
        username = request.POST["username"]
        context = {
            "users": User.objects.filter(username=username),
            "requests": requests
        }
        return render(request, "flights/index.html", context)

def myprofile(request):        
    if request.method == 'POST':
        firstName = request.POST["first"]
        lastName = request.POST["last"]
        bioData = request.POST["bio"]
        dob = request.POST["date"]
        profile = Profile(user=request.user, first=firstName, last=lastName, bio=bioData, birthdate=dob)
        profile.save()
        
        context={
            "username": request.user.username,
            "first": profile.first,
            "last": profile.last,
            "bio": profile.bio,
            "date": profile.birthdate
        }    
        return render(request, "flights/profileDisplay.html", context)    

    
    if request.method == 'GET':
        try:
            profile = Profile.objects.get(user_id=request.user.id)
        except Profile.DoesNotExist:
            context = {
                "username": "Create a profile",
                "first": "You may choose to enter your first name",
                "last": "You may choose to enter your first name",
                "bio": "You may choose to enter your bio",
                "date": "You must be above the age of 16 to register for this site"

            }
            return render(request, "flights/profileCreate.html", context)
        context2={
            "username": request.user.username,
            "first": profile.first,
            "last": profile.last,
            "bio": profile.bio,
            "date": profile.birthdate
        }    
        return render(request, "flights/profileDisplay.html", context2)    

    
    context = {
        "first": first
    }
    return render(request, "flights/profile.html", context)


def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request,user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "flights/login.html", {"message": "invalid credentials"})

def logout_view(request):
    logout(request)
    return render(request, "flights/logout.html", {"message": "Logged out"})


def flight(request, flight_id):
    try:
        flight = Flight.objects.get(pk=flight_id)
    except Flight.DoesNotExist:
        raise Http404("Flight doesn't exist ")
    context={
        "flight": flight,
        "passengers": flight.passengers.all(),
        "non_passengers": Passenger.objects.exclude(flights=flight).all()
    }
    return render(request, "flights/flight.html", context)

def book(request, flight_id):
    try:
        passenger_id = int(request.POST["passenger"])
        passenger = Passenger.objects.get(pk=passenger_id)
        flight = Flight.objects.get(pk=flight_id)
    except KeyError:
        return render(request, "flights/error.html", {"message": "NO pass"})    
    except Passenger.DoesNotExist:
        return render(request,"flights/error.html", {"message": "No passenger"})
    except Flight.DoesNotExist:
        return render(request, "flights/error.html", {"message": "No flight "})   

    passenger.flights.add(flight)
    return HttpResponseRedirect(reverse("flight", args=(flight_id,)))
