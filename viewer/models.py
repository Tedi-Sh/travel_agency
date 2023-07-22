from django.db.models import IntegerField, CharField, ForeignKey, RESTRICT, TextField, Model, DO_NOTHING
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import DateField


class Country(Model):
    name = CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class City(Model):
    name = CharField(max_length=50)
    belong_to_country = ForeignKey(Country, on_delete=RESTRICT)

    def __str__(self):
        return f"{self.name}"


class Hotel(Model):
    name = CharField(max_length=100)
    stars = IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    descriptions = TextField(max_length=255)
    belong_to_city = ForeignKey(City, on_delete=RESTRICT)
    price = IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.name}"


class Airport(Model):
    name = CharField(max_length=100)
    belong_to_city = ForeignKey(City, on_delete=RESTRICT)
    price = IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.name}"


class Trip(Model):

    from_city = ForeignKey(City, related_name='departure_trips', on_delete=DO_NOTHING)
    from_airport = ForeignKey(Airport, related_name='departure_trips', on_delete=DO_NOTHING)
    to_city = ForeignKey(City, related_name='arrival_trips', on_delete=DO_NOTHING)
    to_airport = ForeignKey(Airport, related_name='arrival_trips', on_delete=DO_NOTHING)
    departure_date = DateField()
    return_date = DateField()

    nr_adults = IntegerField()
    places_for_children = IntegerField()

