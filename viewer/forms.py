from django.core.exceptions import ValidationError
from django.db.models import Model, ForeignKey, RESTRICT
from django.forms import DateField, CharField, IntegerField

from viewer.models import City, Airport


class Trip(Model):
    Board_TYPES = [
        ('BB', 'Bed and Breakfast'),
        ('HB', 'Half Board'),
        ('FB', 'Full Board'),
        ('AI', 'All Inclusive')
    ]
    from_city = ForeignKey(City, related_name='departure_trips', on_delete=RESTRICT)
    from_airport = ForeignKey(Airport, related_name='departure_trips', on_delete=RESTRICT)
    to_city = ForeignKey(City, related_name='arrival_trips', on_delete=RESTRICT)
    to_airport = ForeignKey(Airport, related_name='arrival_trips', on_delete=RESTRICT)
    departure_date = DateField()
    return_date = DateField()
    board_type = CharField(max_length=2, choices=Board_TYPES)
    places_for_adults = IntegerField()
    places_for_children = IntegerField()

    def date_check(self):
        if self.return_date <= self.departure_date:
            raise ValidationError('Error')
