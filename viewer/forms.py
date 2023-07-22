from django.core.exceptions import ValidationError
from django.forms import DateField, CharField, IntegerField, Form, SelectDateWidget, ChoiceField, ModelChoiceField

from viewer.models import City, Hotel


class SearchForm(Form):
    TRIP_TYPE_CHOICES = [
        ('BB', 'Bed & Breakfast'),
        ('HB', 'Half Board'),
        ('FB', 'Full Board'),
        ('AI', 'All Inclusive')
    ]

    from_city = ModelChoiceField(queryset=City.objects.all(), label='From')
    to_city = ModelChoiceField(queryset=City.objects.all(), label='To')
    hotel = ModelChoiceField(queryset=Hotel.objects.all(), required=False, label='Hotel')
    departure_date = DateField(widget=SelectDateWidget, label='Departure Date')
    return_date = DateField(widget=SelectDateWidget, label='Return Date')
    trip_type = ChoiceField(choices=TRIP_TYPE_CHOICES, label='Trip Type')
    num_adults = IntegerField(min_value=1, label='Number of Adults')
    num_children = IntegerField(min_value=0, label='Number of Children')

    # class Trip(Model):
    #     Board_TYPES = [
    #         ('BB', 'Bed and Breakfast'),
    #         ('HB', 'Half Board'),
    #         ('FB', 'Full Board'),
    #         ('AI', 'All Inclusive')
    #     ]
    #     from_city = ForeignKey(City, related_name='departure_trips', on_delete=RESTRICT)
    #     from_airport = ForeignKey(Airport, related_name='departure_trips', on_delete=RESTRICT)
    #     to_city = ForeignKey(City, related_name='arrival_trips', on_delete=RESTRICT)
    #     to_airport = ForeignKey(Airport, related_name='arrival_trips', on_delete=RESTRICT)
    #     departure_date = DateField()
    #     return_date = DateField()
    #     board_type = CharField(max_length=2, choices=Board_TYPES)
    #     nr_adults = IntegerField()
    #     places_for_children = IntegerField()

    def date_check(self):
        if self.return_date <= self.departure_date:
            raise ValidationError('Error')
