from django.forms import (
    IntegerField, Form, ChoiceField, ModelChoiceField,
    Select, DateField, SelectDateWidget, NumberInput
)
from viewer.models import City


class SearchForm(Form):
    TRIP_TYPES = [
        ('BB', 'Bed & Breakfast'),
        ('HB', 'Half Board'),
        ('FB', 'Full Board'),
        ('AI', 'All Inclusive')
    ]
    from_location = ModelChoiceField(queryset=City.objects.all(), widget=Select(attrs={'class': 'form-control'}))
    to_location = ModelChoiceField(queryset=City.objects.all(), widget=Select(attrs={'class': 'form-control'}))
    date_of_departure = DateField(widget=SelectDateWidget(attrs={'class': 'form-control'}))
    return_date = DateField(widget=SelectDateWidget(attrs={'class': 'form-control'}))
    number_of_adults = IntegerField(min_value=1, widget=NumberInput(attrs={'class': 'form-control'}))
    number_of_children = IntegerField(min_value=0, widget=NumberInput(attrs={'class': 'form-control'}))
    trip_type = ChoiceField(choices=TRIP_TYPES, widget=Select(attrs={'class': 'form-control'}))

# class SearchForm(Form):
#     TRIP_TYPE_CHOICES = [
#         ('BB', 'Bed & Breakfast'),
#         ('HB', 'Half Board'),
#         ('FB', 'Full Board'),
#         ('AI', 'All Inclusive')
#     ]
#
#     from_city = ModelChoiceField(queryset=City.objects.all())
#     to_city = ModelChoiceField(queryset=City.objects.all())
#     num_adults = IntegerField(min_value=1)
#     num_children = IntegerField(min_value=0)
#     trip_type = ChoiceField(choices=TRIP_TYPE_CHOICES)
