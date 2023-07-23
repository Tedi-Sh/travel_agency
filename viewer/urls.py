from django.urls import path
from .views import search, create_reservation, trips_view

urlpatterns = [
    path('search/', search, name='search'),
    path('create_reservation/', create_reservation, name='create_reservation'),
    path('trips_view/', trips_view, name='trips_view')

]
