import json
from django.core.management import BaseCommand

from viewer.models import Country, City


class CommandCountry(BaseCommand):
    def handle(self, *args, **options):
        with open(r'C:\Users\tedis\OneDrive\Desktop\Travel\city_country_codes.json', 'r') as file:
            data = json.load(file)
            for item in data:
                if not Country.objects.filter(name=item["country"]).exists():
                    Country.objects.create(name=item["country"])
                else:
                    print(item["country"] + " already exists.")


# class CommandCity(BaseCommand):
#     def handle(self, *args, **options):
#         with open(r'C:\Users\tedis\OneDrive\Desktop\Travel\city_country_codes.json', 'r') as file:
#             data = json.load(file)
#             for item in data:
#                 if not City.objects.filter(name=item["city"]).exists():
#                     City.objects.create(name=item["city"])
#                     City.objects.create(belong_to_country_id=Country.objects.id)
#                 else:
#                     print(item["country"] + " already exists.")
