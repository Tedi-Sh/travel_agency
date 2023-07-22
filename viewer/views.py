from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from viewer.forms import SignUpForm, SearchForm
from viewer.models import Hotel


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
            trip_type = form.cleaned_data.get('trip_type')  # optional connected to Class Hotel(Model)
            hotels = Hotel.objects.filter(belong_to_city=to_location)  # , trip_type=trip_type)
            return render(request, 'search_results.html', {
                'hotels': hotels
            })
    else:
        form = SearchForm()
    return render(request, 'search_bar.html', {'form': form})
