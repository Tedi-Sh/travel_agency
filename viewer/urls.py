from django.urls import path
from .views import search, trips_view,create_reservation

urlpatterns = [
    path('search/', search, name='search'),
    path('create_reservation/<hotel_id>', create_reservation, name='create_reservation'),
    path('trips_view/', trips_view, name='trips_view'),
    #path('search_result/',search, name='search_result' )

]
