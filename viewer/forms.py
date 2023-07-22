from django.core.exceptions import ValidationError
from django.forms import (
    IntegerField, Form, ChoiceField, ModelChoiceField,
    Select, DateField, SelectDateWidget, NumberInput, CharField, TextInput
)
from viewer.models import City, Airport, Country
from django.utils.translation import gettext_lazy as _


class SearchForm(Form):
    TRIP_TYPES = [
        ('BB', 'Bed & Breakfast'),
        ('HB', 'Half Board'),
        ('FB', 'Full Board'),
        ('AI', 'All Inclusive')
    ]

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        get_airports = Airport.objects.all()
        self.fields['from_location'] = ChoiceField(
            choices=[(airport.id, f'{airport.belong_to_city.name} - {airport.name}')
                     for airport in get_airports
                     ],
            widget=Select(attrs={'class': 'form-control'}),
            label='From'
        )

        self.fields['to_location'] = ChoiceField(
            choices=[(airport.id, f'{airport.belong_to_city.name} - {airport.name}')
                     for airport in get_airports
                     ],
            widget=Select(attrs={'class': 'form-control'}),
            label='To'
        )

    date_of_departure = DateField(widget=SelectDateWidget(attrs={'class': 'form-control'}))
    return_date = DateField(widget=SelectDateWidget(attrs={'class': 'form-control'}))
    number_of_adults = IntegerField(min_value=1, widget=NumberInput(attrs={'class': 'form-control'}),
                                    label='Nr. of Adults', initial=1)
    number_of_children = IntegerField(min_value=0, widget=NumberInput(attrs={'class': 'form-control'}),
                                      label='Nr. of Children', initial=0)
    trip_type = ChoiceField(choices=TRIP_TYPES, widget=Select(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        date_of_departure = cleaned_data.get('date_of_departure')
        return_date = cleaned_data.get('return_date')

        if date_of_departure and return_date:
            if return_date < date_of_departure:
                raise ValidationError({
                    'return_date': ValidationError(
                        _('Return date cannot be before departure date.'),
                        code='invalid'
                    ),
                })
