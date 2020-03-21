from django.urls import path
from . import views

app_name = 'plots'

urlpatterns = [
    path('', views.home, name='Home'),
    path('resultsplot/', views.resultsplot, name='resultsplot'),
    path('registrar/', views.signup, name='registrar'),
    path('logout/', views.logoutview, name='logout'),
    path('user_login/', views.user_login, name='user_login'),
]
