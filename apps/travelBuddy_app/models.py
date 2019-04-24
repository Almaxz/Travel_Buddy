from django.db import models
from datetime import datetime
import bcrypt

class TravelerManager(models.Manager):
    def reg_validator(self, data):
        errors = {}
        
        if len(data['name']) < 3:
            errors['name'] = "Name must be at least 3 characters"

        if len(data['username']) < 3:
            errors['username'] = "Username must be at least 3 characters"

        elif len(Traveler.objects.filter(username=data['username'])) > 0:
            errors['username'] = "Username already exists"

        if len(data['password']) < 8:
            errors['password'] = "Password must be at least 8 characters" 

        elif data['password'] != data['pw_confirmation']:
            errors['password'] = "Passwords do not match"

        return errors

    def login_validator(self, request):
        
        errors = {}

        if len(request.POST['password']) < 1:
            errors['password'] = "Password cannot be blank"

        if len(request.POST['username']) < 1:
            errors['username'] = "Username cannot be blank"

        elif len(Traveler.objects.filter(username = request.POST['username'])) < 1:
            errors['username']  = "Your username is inaccurate, please enter a correct username or register before attempting to login"

        else:
            traveler = Traveler.objects.get(username = request.POST['username'])
            if not bcrypt.checkpw(request.POST['password'].encode(), traveler.password.encode()):
                errors['password'] = "Your password was entered incorrectly, please try again"
            else:
                request.session['traveler_id'] = traveler.id

        return errors

class TripManager(models.Manager):
    def desination_validator(self, data):
        errors = {}
        if len(data['desination']) < 1:
            errors['desination'] = "Desination cannot be empty"

        if len(data['desc']) < 1:
            errors['desc'] = "Description cannot be empty"

        if len(data['start_date']) < 1:
            errors['start_date'] = "Please enter a start date"

        elif datetime.strptime(data['start_date'], '%Y-%m-%d') < datetime.now():
            errors['start_date'] = 'Traveling back in time is strictly forbidded! Please pick a future start date!' 

        if len(data['end_date']) < 1:
            errors['end_date'] = "Please enter a end date"

        elif datetime.strptime(data['end_date'], '%Y-%m-%d') < datetime.now():
            errors['end_date'] = 'Please choose a future End date!' 
            
        elif datetime.strptime(data['end_date'], '%Y-%m-%d') == datetime.strptime(data['start_date'], '%Y-%m-%d'):
            errors['end_date'] = 'End date and Start date cannot be the same'
        
        elif datetime.strptime(data['end_date'], '%Y-%m-%d') < datetime.strptime(data['start_date'], '%Y-%m-%d'):
            errors['end_date'] = 'End date cannot be before your Start date'
        
        return errors

class Traveler(models.Model): 
    name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = TravelerManager()

class Trip(models.Model):
    desination = models.CharField(max_length = 255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    travel_plans = models.ManyToManyField(Traveler, related_name = "travel_plans")
    plannedby = models.ForeignKey(Traveler, related_name = "plannedbys", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = TripManager()

    def __repr__(self):
        return f"<Trip object: {self.id} ({self.id})>"
