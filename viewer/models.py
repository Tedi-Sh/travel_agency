
from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator


class Country(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class City(models.Model):
    name = models.CharField(max_length=50)
    belong_to_country = models.ForeignKey(Country, on_delete=models.RESTRICT)

    def __str__(self):
        return f"{self.name}"


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    stars = models.IntegerField(validators=[MinLengthValidator(0), MaxLengthValidator(5)])

    descriptions = models.TextField(null=False)
    belong_to_city = models.ForeignKey(City, on_delete=models.RESTRICT)
    price = models.IntegerField(null=False)

    def __str__(self):
        return f"{self.name}"


class Airport(models.Model):
    name = models.CharField(max_length=100, null=False)
    belong_to_city = models.ForeignKey(City, on_delete=models.RESTRICT)
    price = models.IntegerField(null=False)

    def __str__(self):
        return f"{self.name}"


class Price(models.Model):
    airport_price = models.ForeignKey(Airport, related_name='airport_price', on_delete=models.RESTRICT)
    hotel_price = models.ForeignKey(Hotel, related_name='hotel_price', on_delete=models.RESTRICT)










