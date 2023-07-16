from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import (
    RESTRICT, DO_NOTHING, CharField, DateField, DateTimeField, ForeignKey, IntegerField,
    Model, TextField
)


# Create your models here.

class Country(Model):
    name = CharField(max_length=128)  # , blank=False, null=False)

    def __str__(self):
        return self.name


class City(Model):
    name = CharField(max_length=128)  # , blank=False, null=False)
    country = ForeignKey(Country, on_delete=RESTRICT)

    def __str__(self):
        return self.name


class Hotel(Model):
    name = CharField(max_length=128)  # , blank=False, null=False)
    stars = IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = TextField()
    city = ForeignKey(City, on_delete=RESTRICT)

    def __str__(self):
        return self.name


class Airport(Model):
    name = CharField(max_length=128)
    city = ForeignKey(City, on_delete=RESTRICT)

    def __str__(self):
        return self.name


