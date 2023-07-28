from django.contrib.auth.models import User
from django.db.models import IntegerField, CharField, ForeignKey, RESTRICT, TextField, Model, DO_NOTHING, DateField, \
    DecimalField, FloatField
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date


class Country(Model):
    name = CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class City(Model):
    name = CharField(max_length=50)
    belong_to_country = ForeignKey(Country, on_delete=RESTRICT)

    def __str__(self):
        return f"{self.name}"


class Discount(Model):
    age_from = IntegerField(validators=[MinValueValidator(0)])
    age_to = IntegerField(validators=[MinValueValidator(0)])
    discount_percentage = DecimalField(max_digits=5, decimal_places=2,
                                       validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return f"Discount for ages {self.age_from} - {self.age_to}: {self.discount_percentage}%"


class Hotel(Model):
    name = CharField(max_length=100)
    stars = IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    descriptions = TextField(max_length=255)
    belong_to_city = ForeignKey(City, on_delete=RESTRICT)
    price = IntegerField(validators=[MinValueValidator(1)])
    discount = ForeignKey(Discount, null=True, blank=True, on_delete=RESTRICT)

    def __str__(self):
        return f"{self.name}"


class Airport(Model):
    name = CharField(max_length=100)
    belong_to_city = ForeignKey(City, on_delete=RESTRICT)
    price = IntegerField(validators=[MinValueValidator(1)])
    discount = ForeignKey(Discount, null=True, blank=True, on_delete=RESTRICT)

    def __str__(self):
        return f"{self.name}"


class Trip(Model):
    from_city = ForeignKey(City, related_name='departure_trips', on_delete=DO_NOTHING)
    from_airport = ForeignKey(Airport, related_name='departure_trips', on_delete=DO_NOTHING)
    to_city = ForeignKey(City, related_name='arrival_trips', on_delete=DO_NOTHING)
    to_airport = ForeignKey(Airport, related_name='arrival_trips', on_delete=DO_NOTHING)
    departure_date = DateField(auto_created=False, default=date.today())
    return_date = DateField(auto_created=False, default=date.today())

    nr_adults = IntegerField(default=1)
    places_for_children = IntegerField(default=0)

    def __str__(self):
        return f"{self.from_city} to {self.to_city}"


class Reservations(Model):
    user = ForeignKey(User, on_delete=DO_NOTHING)
    from_location = ForeignKey(City, related_name='departure_cities', on_delete=DO_NOTHING)
    to_location = ForeignKey(City, related_name='arrival_cities', on_delete=DO_NOTHING)
    from_airport = ForeignKey(Airport, related_name='departure_airports', on_delete=DO_NOTHING)
    to_airport = ForeignKey(Airport, related_name='arrival_airports', on_delete=DO_NOTHING)
    date_of_departure = DateField()
    return_date = DateField()
    number_of_adults = IntegerField(validators=[MinValueValidator(1)])
    number_of_children = IntegerField(validators=[MinValueValidator(0)])
    hotel = ForeignKey(Hotel, on_delete=DO_NOTHING)
    hotel_price = FloatField(default=0)
    airport_price = FloatField(default=0)

    def __str__(self):
        return f"Reservation by {self.from_location.name} to {self.to_location.name}"

