from django.urls import path
from .views import search, create_reservation, trips_view, register_user, login, log_out, about_us

urlpatterns = [
    path('search/', search, name='search'),
    path('create_reservation/<int:hotel_id>/', create_reservation, name='create_reservation'),
    path('trips_view/', trips_view, name='trips_view'),
    path('aboutus/', about_us, name='aboutus'),
    path('register/', register_user, name='register_user'),
    path('login/', login, name='login'),
    path('logout/', log_out, name='log_out')]
