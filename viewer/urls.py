from django.urls import path
from .views import search, create_reservation, trips_view, register_user, login, log_out, about_us, reservations_view, \
    delete_reservation, fetch_city_data, book_trip, ReservationUpdateView

urlpatterns = [
    path('search/', search, name='search'),
    path('create_reservation/<int:hotel_id>/', create_reservation, name='create_reservation'),
    path('trips_view/', trips_view, name='trips_view'),
    path('register/', register_user, name='register_user'),
    path('accounts/login/', login, name='login'),
    path('login/', login, name='login'),
    path('logout/', log_out, name='log_out'),
    path('aboutus/', about_us, name='aboutus'),
    path('reservations/', reservations_view, name='reservations'),
    path('delete_reservation/<int:reservation_id>/', delete_reservation, name='delete_reservation'),
    path('fetch_city_data/<int:city_id>/', fetch_city_data, name='fetch_city_data'),
    path('book_trip/<int:trip_id>/', book_trip, name='book_res'),
    path('modify_reservation/<int:pk>', ReservationUpdateView.as_view(), name='modify_reservation'),
]
