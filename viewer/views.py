from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from viewer.forms import SearchForm
from viewer.models import Hotel, Airport


def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            from_city = form.cleaned_data['from_city']
            to_city = form.cleaned_data['to_city']
            hotel = form.cleaned_data['hotel']
            departure_date = form.cleaned_data['departure_date']
            return_date = form.cleaned_data['return_date']
            trip_type = form.cleaned_data['trip_type']
            num_adults = form.cleaned_data['num_adults']
            num_children = form.cleaned_data['num_children']

            # Perform the search
            # Use the cleaned_data to search for matching trips
            # This will vary based on your models and database setup
            # Here is a very basic example, you will need to adjust it to fit your needs
            hotels = Hotel.objects.filter(city=to_city)
            airports = Airport.objects.filter(city=from_city)

            # Then pass these results to your template
            return render(request, 'results.html', {'hotels': hotels, 'airports': airports})

    else:
        form = SearchForm()
    return render(request, 'search.html', {'form': form})
