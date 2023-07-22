from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SignUpForm


from django.contrib import messages


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
    #message.reques("You have logged out")
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
            #messages.request("Record created)
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html',{'form': form})
    return render(request, 'register.html',{'form': form})



# def Trip(request):
#     form = AddTrip()
#     if request.method == "POST":
#         form = AddTrip(request.POST)
#         if form.is_valid():
#             form.save()
#             return render(request, 'show_offers.html')
#
#     context = {'form': form}
#     return render(request, 'add_trip.html', context)






















# def search(request):
#     if request.method == 'POST':
#         form = SearchForm(request.POST)
#         if form.is_valid():
#             from_city = form.cleaned_data['from_city']
#             to_city = form.cleaned_data['to_city']
#             hotel = form.cleaned_data['hotel']
#             departure_date = form.cleaned_data['departure_date']
#             return_date = form.cleaned_data['return_date']
#             trip_type = form.cleaned_data['trip_type']
#             num_adults = form.cleaned_data['num_adults']
#             num_children = form.cleaned_data['num_children']
#
#             # Perform the search
#             # Use the cleaned_data to search for matching trips
#             # This will vary based on your models and database setup
#             # Here is a very basic example, you will need to adjust it to fit your needs
#             hotels = Hotel.objects.filter(city=to_city)
#             airports = Airport.objects.filter(city=from_city)
#
#             # Then pass these results to your template
#             return render(request, 'test_result.html', {'hotels': hotels, 'airports': airports})
#
#     else:
#         form = SearchForm()
#     return render(request, 'test_search.html', {'form': form})
