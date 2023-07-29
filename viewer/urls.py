from django.urls import path
from .views import search, create_reservation, trips_view, register_user, login, log_out, about_us, book_trip

urlpatterns = [
    path('search/', search, name='search'),
    path('create_reservation/<int:hotel_id>/', create_reservation, name='create_reservation'),
    path('trips_view/', trips_view, name='trips_view'),
    path('register/', register_user, name='register_user'),
    path('login/', login, name='login'),
    path('logout/', log_out, name='log_out'),
    path('aboutus/', about_us, name='aboutus'),
    path('book_trip/<int:trip_id>/', book_trip, name='book_res'),

    # path('search_results/', search, name='search_results')

]
