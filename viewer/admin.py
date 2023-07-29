from django.contrib import admin
from .models import Trip, Discount, Reservations

admin.site.register(Trip)
admin.site.register(Discount)
admin.site.register(Reservations)
