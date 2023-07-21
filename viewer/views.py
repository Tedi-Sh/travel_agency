from django.shortcuts import render
from viewer.models import Hotel, Airport
from .forms import SearchForm


def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            # Get data from form
            from_location = form.cleaned_data.get('from_location')
            to_location = form.cleaned_data.get('to_location')
            date_of_departure = form.cleaned_data.get('date_of_departure')
            return_date = form.cleaned_data.get('return_date')
            number_of_adults = form.cleaned_data.get('number_of_adults')
            number_of_children = form.cleaned_data.get('number_of_children')
            trip_type = form.cleaned_data.get('trip_type')

            # Query hotels and airports based on data
            hotels = Hotel.objects.filter(belong_to_city=to_location)
            airports = Airport.objects.filter(belong_to_city__in=[from_location, to_location])

            # Render the results template with queried data
            return render(request, 'search_results.html', {
                'hotels': hotels,
                'airports': airports,
            })
    else:
        form = SearchForm()

    return render(request, 'search.html', {'form': form})
