from django.urls import path
from . import views
from .views import search

urlpatterns = [
    # path('', views.home, name='home'),
    path('search/', search, name='search'),

]
