from django.db.models import IntegerField, CharField, ForeignKey, RESTRICT, TextField
from django.core.validators import MinLengthValidator, MaxLengthValidator


class Country:
    name = CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class City:
    name = CharField(max_length=50)
    belong_to_country = ForeignKey(Country, on_delete=RESTRICT)

    def __str__(self):
        return f"{self.name}"


class Hotel:
    name = CharField(max_length=100)
    stars = IntegerField(validators=[MinLengthValidator(0), MaxLengthValidator(5)])

    descriptions = TextField(max_length=255)
    belong_to_city = ForeignKey(City, on_delete=RESTRICT)
    price = IntegerField(validators=[MinLengthValidator(1)])

    def __str__(self):
        return f"{self.name}"


class Airport:
    name = CharField(max_length=100)
    belong_to_city = ForeignKey(City, on_delete=RESTRICT)
    price = IntegerField(validators=[MinLengthValidator(1)])

    def __str__(self):
        return f"{self.name}"


class Price:
    airport_price = ForeignKey(Airport, related_name='airport_price', on_delete=RESTRICT)
    hotel_price = ForeignKey(Hotel, related_name='hotel_price', on_delete=RESTRICT)
