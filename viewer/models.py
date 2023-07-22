from django.db.models import IntegerField, CharField, ForeignKey, RESTRICT, TextField, Model
from django.core.validators import MinValueValidator, MaxValueValidator


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


class Price(Model):
    airport_price = ForeignKey(Airport, related_name='airport_price', on_delete=RESTRICT)
    hotel_price = ForeignKey(Hotel, related_name='hotel_price', on_delete=RESTRICT)
