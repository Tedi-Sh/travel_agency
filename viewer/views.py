from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from viewer.forms import SignUpForm, SearchForm
from viewer.models import Hotel, Airport, Trip, City, Country
from django.contrib.auth.decorators import login_required
from .models import Reservations
from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login


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
    # message.reques("You have logged out")
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
            # messages.request("Record created)
            return redirect('search')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})


# def search(request):
#     if request.method == "POST":
#         form = SearchForm(request.POST)
#         if form.is_valid():
#             to_location = form.cleaned_data.get('to_location')
#             destination_airport = Airport.objects.get(pk=to_location)
#             hotels = Hotel.objects.filter(belong_to_city=destination_airport.belong_to_city)
#             return render(request, 'search_results.html', {
#                 'hotels': hotels
#             })
#     else:
#         form = SearchForm()
#
#     return render(request, 'search.html', {'form': form})
#
#
# @login_required
# def search_view(request):
#     if request.method == "POST":
#         form = SearchForm(request.POST)
#         if form.is_valid():
#             from_location = form.cleaned_data.get('from_location')
#             to_location = form.cleaned_data.get('to_location')
#             date_of_departure = form.cleaned_data.get('date_of_departure')
#             return_date = form.cleaned_data.get('return_date')
#             number_of_adults = form.cleaned_data.get('number_of_adults')
#             number_of_children = form.cleaned_data.get('number_of_children')
#
#             try:
#                 from_airport = Airport.objects.get(pk=from_location)
#                 to_airport = Airport.objects.get(pk=to_location)
#
#                 # Store these details in the session
#                 request.session['reservation_details'] = {
#                     'from_location': from_airport.id,
#                     'to_location': to_airport.id,
#                     'date_of_departure': date_of_departure.isoformat(),
#                     'return_date': return_date.isoformat(),
#                     'number_of_adults': number_of_adults,
#                     'number_of_children': number_of_children
#                 }
#
#                 # Redirect to the results page
#                 return HttpResponseRedirect('/search_results/')
#             except Airport.DoesNotExist:
#                 form.add_error(None, 'Invalid airport selected')
#     else:
#         form = SearchForm()
#
#     return render(request, 'search.html', {'form': form})
#
#
# @login_required
# def create_reservation_view(request, hotel_id):
#     # Retrieve the reservation details from the session
#     details = request.session.get('reservation_details')
#
#     if not details:
#         return HttpResponseRedirect(reverse('search'))  # Use 'reverse' to avoid hard-coding URLs
#
#     hotel = get_object_or_404(Hotel, pk=hotel_id)  # Use 'get_object_or_404' to simplify error handling
#     from_location = get_object_or_404(Airport, pk=details['from_location'])
#     to_location = get_object_or_404(Airport, pk=details['to_location'])
#
#     reservation = Reservations.objects.create(
#         user=request.user,
#         from_location=from_location,
#         to_location=to_location,
#         date_of_departure=datetime.fromisoformat(details['date_of_departure']),
#         return_date=datetime.fromisoformat(details['return_date']),
#         number_of_adults=details['number_of_adults'],
#         number_of_children=details['number_of_children'],
#         hotel=hotel
#     )
#
#     # Clear the reservation details from the session
#     del request.session['reservation_details']
#
#     return render(request, 'reservation_success.html', {'reservation': reservation})

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
            # from_airport = form.cleaned_data.get('from_airport')
            # to_airport = form.cleaned_data.get('to_airport')
            destination_airport = Airport.objects.get(pk=to_location)
            hotel = Hotel.objects.filter(belong_to_city=destination_airport.belong_to_city)
            # Store these details in the session
            request.session['reservation_details'] = {
                # 'from_airport': from_airport,
                # 'to_airport': to_airport,
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
    return render(request, 'reservations.html', {'reservation': reservation})


def about_us(request):
    return render(request, 'about_us.html')
