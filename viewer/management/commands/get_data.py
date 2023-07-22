import json
from random import randint, shuffle, choice

from django.core.management import BaseCommand

from viewer.models import Country, City, Airport, Hotel


# class Command(BaseCommand):
#     def handle(self, *args, **options):
#         with open(r'C:\Users\tedis\OneDrive\Desktop\Travel\city_country_codes.json', 'r') as file:
#             data = json.load(file)
#             for item in data:
#                 if not Country.objects.filter(name=item["country"]).exists():
#                     Country.objects.create(name=item["country"])
#                 else:
#                     print(item["country"] + " already exists.")


# class Command(BaseCommand):
#     def handle(self, *args, **options):
#         with open(r'C:\Users\tedis\OneDrive\Desktop\Travel\city_country_codes.json', 'r') as file:
#             data = json.load(file)
#             for item in data:
#                 if not City.objects.filter(name=item["city"]).exists():
#                     country = Country.objects.get(name=item['country'])
#                     City.objects.create(name=item["city"], belong_to_country_id=country.id)
#                 else:
#                     print(item["city"] + " already exists.")


# class Command(BaseCommand):
#     def handle(self, *args, **options):
#         with open(r'C:\Users\tedis\OneDrive\Desktop\Travel\city_country_codes.json', 'r') as file:
#             data = json.load(file)
#             for item in data:
#                 if not Airport.objects.filter(name=item["Airport_code"]).exists():
#                     city = City.objects.get(name=item["city"])
#                     price = randint(1, 2000)
#                     Airport.objects.create(name=item["Airport_code"], belong_to_city=city, price=price)
#                 else:
#                     print(item["Airport_code"] + " already exists.")
#
class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(r'C:\Users\tedis\OneDrive\Desktop\Travel\hotels.json', 'r') as file:
            data = json.load(file)

            # get list of all city instances
            all_cities = list(City.objects.all())

            # shuffle the list to randomize the order
            shuffle(all_cities)

            # make sure that we have enough cities for the hotels
            if len(data) < len(all_cities):
                raise Exception(
                    "There are more cities than hotels. Please add more hotels or reduce the number of cities.")

            # ensure each city has at least one hotel
            for i in range(len(all_cities)):
                item = data[i]
                if not Hotel.objects.filter(name=item["name"]).exists():
                    Hotel.objects.create(name=item["name"], stars=item['stars'], descriptions=item['descriptions'],
                                         price=item['price'], belong_to_city=all_cities[i])
                else:
                    print(item["name"] + " name exists.")

            # for the remaining hotels, assign a random city
            for item in data[len(all_cities):]:
                if not Hotel.objects.filter(name=item["name"]).exists():
                    Hotel.objects.create(name=item["name"], stars=item['stars'], descriptions=item['descriptions'],
                                         price=item['price'], belong_to_city=choice(all_cities))
                else:
                    print(item["name"] + " name exists.")
