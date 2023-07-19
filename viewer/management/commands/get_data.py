import json
from django.core.management import BaseCommand

from viewer.models import Country, City, Airport


# class Command(BaseCommand):
#     def handle(self, *args, **options):
#         with open(r'C:\Users\Tomas Arapi\Desktop\travel\city_country_codes.json', 'r') as file:
#             data = json.load(file)
#             for item in data:
#                 if not Country.objects.filter(name=item["country"]).exists():
#                     Country.objects.create(name=item["country"])
#                 else:
#                     print(item["country"] + " already exists.")


# class Command(BaseCommand):
#     def handle(self, *args, **options):
#         with open(r'C:\Users\Tomas Arapi\Desktop\travel\city_country_codes.json', 'r') as file:
#             data = json.load(file)
#             for item in data:
#                 ids = Country.objects.get(name=item['country'])
#                 City.objects.create(name=item['city'], belong_to_country_id=ids.id)
#             print(City.objects.all())

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(r'C:\Users\Tomas Arapi\Desktop\travel\city_country_codes.json', 'r') as file:
            data = json.load(file)

            for item in data:
                citties = City.objects.get(name=item['city'])
                Airport.objects.create(name=item['city'], )
            #ids = City.objects.values_list('id', flat=True)















            #     citites = City.objects.filter(name=item['city'])
            # for i in citites.values_list('id'):
            #     print(i)
