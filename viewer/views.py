from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from viewer.forms import SignUpForm, SearchForm
from viewer.models import Hotel, Airport, Trip
# from django.contrib.auth.decorators import login_required
from .models import Reservations
from django.shortcuts import render


def trips_view(request):
    trips = Trip.objects.all()[:8]
    return render(request, 'PaketaTuristike.html', {'trips': trips})


def home(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('home')
    else:
        return render(request, 'test_home.html')


def log_out(request):
    logout(request)
    # message.reques("You have logged out")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            # messages.request("Record created)
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})


def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            to_location = form.cleaned_data.get('to_location')
            destination_airport = Airport.objects.get(pk=to_location)
            hotels = Hotel.objects.filter(belong_to_city=destination_airport.belong_to_city)
            return render(request, 'search_results.html', {
                'hotels': hotels
            })
    else:
        form = SearchForm()

    return render(request, 'search.html', {'form': form})


# @login_required
def create_reservation(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            from_location = form.cleaned_data.get('from_location')
            to_location = form.cleaned_data.get('to_location')
            date_of_departure = form.cleaned_data.get('date_of_departure')
            return_date = form.cleaned_data.get('return_date')
            number_of_adults = form.cleaned_data.get('number_of_adults')
            number_of_children = form.cleaned_data.get('number_of_children')

            try:
                from_airport = Airport.objects.get(pk=from_location)
                to_airport = Airport.objects.get(pk=to_location)

                reservation = Reservations.objects.create(
                    # user=request.user,
                    from_location=from_airport,
                    to_location=to_airport,
                    date_of_departure=date_of_departure,
                    return_date=return_date,
                    number_of_adults=number_of_adults,
                    number_of_children=number_of_children
                )

                return render(request, 'reservation_success.html', {'reservation': reservation})
            except Airport.DoesNotExist:
                form.add_error(None, 'Invalid airport selected')
    else:
        form = SearchForm()

    return render(request, 'search.html', {'form': form})
