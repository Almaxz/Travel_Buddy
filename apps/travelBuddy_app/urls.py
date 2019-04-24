from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('travels', views.travels),
    path('logout', views.logout),
    path('travels/add_trip', views.add_trip),
    path('destroy/<trip_id>', views.destroy),
    path('create/<int:traveler_id>', views.create),
    path('unjoin/<trip_id>', views.unjoin),
    path('join_trip/<trip_id>', views.join_trip),
    path('desination_info/<trip_id>', views.desination_info),
]  