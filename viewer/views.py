from django.shortcuts import render
from viewer.models import Hotel, City
from .forms import SearchForm


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


