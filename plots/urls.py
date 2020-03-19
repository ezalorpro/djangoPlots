from django.urls import path
from . import views

app_name = 'plots'

urlpatterns = [
    path('', views.home, name='Home'),
    path('resultsplot/',
         views.resultsplot, name='resultsplot'),
]
