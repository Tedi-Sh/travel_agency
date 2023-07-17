from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.


def home(request):
    return HttpResponse("Hello..........")





class SearchForm:
    pass


def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            pass
    # use form data to perform search
    # you would define your search logic here, depending on your models and database setup
    else:
        form = SearchForm()
    return render(request, 'search.html', {'form': form})
