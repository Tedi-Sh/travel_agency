from django.urls import path
from .views import search, create_reservation, trips_view, register_user, login, log_out, about_us, reservations_view, \
    modify_reservation, delete_reservation, book_trip, fetch_city_data

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
    path('modify_reservation/<int:reservation_id>/', modify_reservation, name='modify_reservation'),
    path('delete_reservation/<int:reservation_id>/', delete_reservation, name='delete_reservation'),
    path('book_trip/<int:trip_id>/', book_trip, name='book_res'),
    path('fetch_city_data/<int:city_id>/', fetch_city_data, name='fetch_city_data'),

    # path('search_results/', search, name='search_results')

]
