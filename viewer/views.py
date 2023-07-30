from datetime import datetime
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.views.generic import UpdateView
from viewer.forms import SignUpForm, SearchForm, ReservationForm
from viewer.models import Hotel, Airport, Trip, City
from .models import Reservations
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def my_profile(request):
    user_name = request.user.username
    return render(request, 'user.html', {'user_name': user_name})


def about_us(request):
    return render(request, 'about_us.html')


def trips_view(request):
    trips = Trip.objects.all()[:8]
    return render(request, 'PaketaTuristike.html', {'trips': trips})


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('search')
        else:
            return redirect('search')
    else:
        return render(request, 'user.html')


def log_out(request):
    logout(request)
    return redirect('search')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            return redirect('search')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})


def fetch_city_data(request, city_id):
    city = get_object_or_404(City, id=city_id)
    hotels = Hotel.objects.filter(belong_to_city=city)

    airport = Airport.objects.filter(belong_to_city=city).first()

    data = {
        'hotels': [{'id': hotel.id, 'name': hotel.name, 'price': hotel.price} for hotel in hotels],
        'airport_price': airport.price if airport else None,
    }

    return JsonResponse(data)


@login_required
def book_trip(request, trip_id):
    try:
        trip = get_object_or_404(Trip, pk=trip_id)
        user = request.user
        to_city = trip.to_city.id
        to_airport = trip.to_airport.id
        from_city = trip.from_city.id
        from_airport = trip.from_airport.id
        airport_price = trip.to_airport.price
        return_date = trip.return_date
        departure_date = trip.departure_date
        hotel = Hotel.objects.filter(belong_to_city=to_airport).first()
        number_of_children = trip.places_for_children
        number_of_adults = trip.nr_adults
        hotel_price = hotel.price
        reservation = Reservations.objects.create(date_of_departure=departure_date,
                                                  return_date=return_date,
                                                  number_of_adults=number_of_adults,
                                                  number_of_children=number_of_children,
                                                  from_location_id=from_city,
                                                  hotel_id=hotel.id,
                                                  to_location_id=to_city,
                                                  user_id=user.id,
                                                  from_airport_id=from_airport,
                                                  to_airport_id=to_airport,
                                                  airport_price=airport_price,
                                                  hotel_price=hotel_price,
                                                  )
        return render(request, "reservation_success.html", {"reservation": reservation})
    except Exception as e:
        return render(request, "error.html", {"error": str(e)})


def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            from_location = form.cleaned_data.get('from_location')
            to_location = form.cleaned_data.get('to_location')
            date_of_departure = form.cleaned_data.get('date_of_departure')
            return_date = form.cleaned_data.get('return_date')
            number_of_adults = form.cleaned_data.get('number_of_adults')
            number_of_children = form.cleaned_data.get('number_of_children')
            destination_airport = Airport.objects.get(pk=to_location)
            hotel = Hotel.objects.filter(belong_to_city=destination_airport.belong_to_city)
            request.session['reservation_details'] = {
                'date_of_departure': date_of_departure.isoformat(),
                'return_date': return_date.isoformat(),
                'number_of_adults': number_of_adults,
                'number_of_children': number_of_children,
                'from_location': from_location,
                'to_location': to_location
            }
            return render(request, 'search_results.html', {'hotels': hotel})
    else:
        form = SearchForm()
    return render(request, 'search.html', {'form': form})


@login_required
def create_reservation(request, hotel_id):
    details = request.session.get('reservation_details')
    if not details:
        return render(request, 'search.html')
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    from_location = get_object_or_404(City, pk=details['from_location'])
    to_location = get_object_or_404(City, pk=details['to_location'])
    from_airport = from_location.airport_set.first()
    to_airport = to_location.airport_set.first()
    hotel_price = hotel.price
    airport_price = to_airport.price
    reservation = Reservations.objects.create(
        user=request.user,
        from_airport=from_airport,
        to_airport=to_airport,
        to_location=to_location,
        from_location=from_location,
        date_of_departure=datetime.fromisoformat(details['date_of_departure']),
        return_date=datetime.fromisoformat(details['return_date']),
        number_of_children=details['number_of_children'],
        number_of_adults=details['number_of_adults'],
        hotel=hotel,
        hotel_price=hotel_price,
        airport_price=airport_price
    )
    del request.session['reservation_details']
    return render(request, 'reservation_success.html', {'reservation': reservation})


def reservations_view(request):
    reservations = Reservations.objects.filter(user=request.user)

    return render(request, 'reservations.html', {'reservations': reservations})


class ReservationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Reservations
    form_class = ReservationForm
    template_name = 'modify_reservation.html'
    success_url = '/reservations'

    def test_func(self):
        reservation = self.get_object()
        return self.request.user == reservation.user


@csrf_exempt
def update_reservation(request):
    if request.method == "POST":
        data = json.loads(request.body)
        return JsonResponse({"message": "Success!"})


@login_required
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservations, id=reservation_id)

    if request.user != reservation.user:
        messages.error(request, 'You are not authorized to delete this reservation.')
        return redirect('reservations')

    if request.method == 'POST':
        reservation.delete()
        messages.success(request, 'Your reservation has been deleted.')
        return redirect('reservations')

    return render(request, 'confirm_delete.html', {'reservation': reservation})
