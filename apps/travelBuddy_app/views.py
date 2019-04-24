from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, "index.html")

def register(request):
    errors = Traveler.objects.reg_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else: 
        hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        traveler = Traveler.objects.create(name = request.POST['name'], username = request.POST['username'], password = hashed)
        request.session['traveler_id'] = traveler.id
        return redirect('/travels')

def login(request):
    errors = Traveler.objects.login_validator(request)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        return redirect('/travels')

def logout(request):
    request.session.clear()
    return redirect('/')

def travels(request):
    if 'traveler_id' not in request.session:
        messages.error(request, "Please Login/Register")
        return redirect('/')
    else: 
        traveler = Traveler.objects.get(id = request.session['traveler_id'])
        trips = Trip.objects.all()

        travel_plans = traveler.travel_plans.all()
        trip_planned = trips.difference(travel_plans)

        context = {
            'traveler': traveler,
            'travel_plans' : travel_plans,
            'trip_planned' : trip_planned, 
        }

        return render(request, 'travels.html', context)

def add_trip(request):
    traveler = Traveler.objects.get(id = request.session['traveler_id'])
    context = {
        'traveler': traveler,
    }
    return render(request, 'addtrip.html', context)

def create(request, traveler_id):
    traveler = Traveler.objects.get(id = traveler_id)
    errors = Trip.objects.desination_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value) 
        return redirect('/travels/add_trip') 

    else:
        trip = Trip.objects.create(desination = request.POST['desination'], description = request.POST['desc'], start_date = request.POST['start_date'], end_date = request.POST['end_date'] , plannedby = traveler)

        traveler.travel_plans.add(trip)

        return redirect('/travels')

def join_trip(request, trip_id):
    traveler = Traveler.objects.get(id = request.session['traveler_id'])
    trip = Trip.objects.get(id = trip_id)
    traveler.travel_plans.add(trip)
    return redirect('/travels')

def unjoin(request, trip_id):
    traveler = Traveler.objects.get(id = request.session['traveler_id'])
    trip = Trip.objects.get(id = trip_id)
    traveler.travel_plans.remove(trip)
    return redirect('/travels')

def desination_info(request, trip_id):
    trip = Trip.objects.get(id = trip_id)
    joiners = trip.travel_plans.all()
    # .exclude(plannedbys = trip)
    context = { 
        'trip': trip,
        'joiners': joiners,
    }
    return render(request, 'desination.html', context)

def destroy(request, trip_id):
    trip = Trip.objects.filter(id = trip_id)
    trip.delete() 
    return redirect('/travels')